"""Cliente de IA con control de costes: enrutado de modelos, topes, caché y registro.

Todas las llamadas a la API de Claude del proyecto pasan por `LLM.run()`:
  1. elige el modelo según config/budget.yaml (routing por tipo de tarea);
  2. estima el coste máximo y aborta si supera el tope por tarea o el mensual;
  3. devuelve la respuesta en caché si la petición idéntica ya se hizo;
  4. registra tokens y coste reales en el ledger CSV.

Requiere ANTHROPIC_API_KEY (u otra credencial del SDK) solo para llamadas reales.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path

from common import ROOT, load_yaml

LEDGER_FIELDS = ["ts", "task", "target", "model", "input_tokens", "output_tokens",
                 "cache_read_tokens", "cache_write_tokens", "cost_usd", "cached"]
# Modelos con fallback del lado del servidor ante rechazos (ver skill claude-api).
FALLBACK_MODELS = {"claude-opus-5-5", "claude-sonnet-5-5"}


class BudgetExceeded(RuntimeError):
    pass


class RefusalError(RuntimeError):
    pass


@dataclass
class Result:
    text: str
    model: str
    cost_usd: float
    cached: bool


def estimate_tokens(text: str) -> int:
    """Estimación conservadora sin red (~3 caracteres por token en español)."""
    return max(1, len(text) // 3)


class LLM:
    def __init__(self, client=None, config_path: Path | None = None, root: Path = ROOT):
        self.root = root
        self.cfg = load_yaml(config_path or root / "config" / "budget.yaml")
        self.prices = self.cfg["pricing_usd_per_mtok"]
        self.limits = self.cfg["limits"]
        self.ledger = root / self.cfg["ledger"]
        self.cache_dir = root / self.cfg["cache"]["dir"]
        self._client = client

    # --- coste -----------------------------------------------------------
    def price(self, model: str, inp: int, out: int, cache_read: int = 0, cache_write: int = 0) -> float:
        p = self.prices[model]
        return (inp * p["input"] + out * p["output"]
                + cache_read * p["input"] * p.get("cache_read_factor", 0.1)
                + cache_write * p["input"] * 1.25) / 1_000_000

    def month_spent(self, today: dt.date | None = None) -> float:
        today = today or dt.date.today()
        if not self.ledger.exists():
            return 0.0
        prefix = today.strftime("%Y-%m")
        with open(self.ledger, encoding="utf-8") as f:
            return sum(float(r["cost_usd"]) for r in csv.DictReader(f) if r["ts"].startswith(prefix))

    def model_for(self, task: str, escalate: bool = False) -> str:
        if escalate and task in self.cfg.get("escalation", {}):
            return self.cfg["escalation"][task]
        return self.cfg["routing"][task]

    def check_budget(self, model: str, prompt_text: str, max_tokens: int) -> float:
        est = self.price(model, estimate_tokens(prompt_text), max_tokens)
        if est > self.limits["per_task_usd"]:
            raise BudgetExceeded(f"coste máximo estimado {est:.3f} USD > tope por tarea {self.limits['per_task_usd']}")
        spent = self.month_spent()
        if spent + est > self.limits["monthly_usd"]:
            raise BudgetExceeded(f"tope mensual: gastado {spent:.2f} + estimado {est:.3f} > {self.limits['monthly_usd']}")
        return est

    # --- caché y registro ---------------------------------------------------
    def _key(self, payload: dict) -> str:
        return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

    def _log(self, task, target, model, inp, out, cr, cw, cost, cached) -> None:
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        new = not self.ledger.exists()
        with open(self.ledger, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
            if new:
                w.writeheader()
            w.writerow({"ts": dt.datetime.now().isoformat(timespec="seconds"), "task": task, "target": target,
                        "model": model, "input_tokens": inp, "output_tokens": out, "cache_read_tokens": cr,
                        "cache_write_tokens": cw, "cost_usd": f"{cost:.6f}", "cached": cached})

    @property
    def client(self):
        if self._client is None:
            import anthropic  # importación diferida: los scripts sin IA no lo necesitan
            self._client = anthropic.Anthropic()
        return self._client

    # --- llamada --------------------------------------------------------------
    def run(self, task: str, system: str, user: str, target: str = "", max_tokens: int | None = None,
            escalate: bool = False, effort: str = "medium") -> Result:
        model = self.model_for(task, escalate)
        max_tokens = min(max_tokens or self.limits["max_output_tokens"], self.limits["max_output_tokens"])
        payload = {"model": model, "system": system, "user": user, "max_tokens": max_tokens, "effort": effort}
        key = self._key(payload)
        cache_file = self.cache_dir / f"{key}.json"
        if self.cfg["cache"]["enabled"] and cache_file.exists():
            data = json.loads(cache_file.read_text(encoding="utf-8"))
            self._log(task, target, model, 0, 0, 0, 0, 0.0, True)
            return Result(data["text"], model, 0.0, True)

        self.check_budget(model, system + user, max_tokens)
        kwargs = dict(
            model=model,
            max_tokens=max_tokens,
            # El prompt de sistema (manual de estilo) es estable: se cachea.
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": user}],
            output_config={"effort": effort},
        )
        if model in FALLBACK_MODELS:
            kwargs.update(betas=["server-side-fallback-2026-07-01"], fallbacks="default")
            resp = self.client.beta.messages.create(**kwargs)
        else:
            resp = self.client.messages.create(**kwargs)
        u = resp.usage
        inp, out = u.input_tokens, u.output_tokens
        cr = getattr(u, "cache_read_input_tokens", 0) or 0
        cw = getattr(u, "cache_creation_input_tokens", 0) or 0
        cost = self.price(model, inp, out, cr, cw)
        self._log(task, target, model, inp, out, cr, cw, cost, False)
        if resp.stop_reason == "refusal":
            raise RefusalError(f"el modelo rechazó la tarea {task} ({target})")
        if resp.stop_reason == "max_tokens":
            raise RuntimeError(f"respuesta truncada por max_tokens en {task} ({target})")
        text = "".join(b.text for b in resp.content if b.type == "text")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps({"text": text, "model": model}, ensure_ascii=False), encoding="utf-8")
        return Result(text, model, cost, False)


def has_credentials() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))
