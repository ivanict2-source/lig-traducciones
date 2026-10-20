import csv
import shutil
import tarfile

import pytest

import analytics_report
import approve
import backup
from pipeline import slugify, validate_draft_body


def test_slugify():
    assert slugify("Métodos de pago en Perú") == "metodos-de-pago-en-peru"


def test_validate_draft_body():
    assert "contiene H1" in validate_draft_body("# Título\n" + "x " * 200)
    assert validate_draft_body("Texto normal. " * 100) == []
    assert "expresión comercial prohibida" in validate_draft_body("Juega gratis. " * 100)


def test_approve_rejects_agents_and_pending(tmp_path):
    src = tmp_path / "x.md"
    shutil.copy("content/guias/co-verificar-licencia-coljuegos.md", src)
    assert approve.approve(src, "agente-redactor", True) == 1
    assert approve.approve(src, "Ana Pérez", True) == 1  # tiene marcadores PENDIENTE


def test_publish_requires_approval(tmp_path):
    src = tmp_path / "x.md"
    shutil.copy("content/guias/senales-casino-no-autorizado.md", src)
    assert approve.publish(src) == 1


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def test_analytics_separates_clicks_and_confirmed_revenue(tmp_path):
    # Datos ficticios de prueba (fixture), no reales.
    write_csv(tmp_path / "gsc" / "g.csv", [
        {"page": "https://x.example/co/", "clicks": "10", "impressions": "100", "ctr": "0.1", "position": "8"}])
    write_csv(tmp_path / "affiliate" / "a.csv", [
        {"date": "2026-10-01", "program": "p", "subid": "co-wplay-co", "clicks": "50", "registrations": "3",
         "ftd": "1", "commission_usd": "40", "status": "confirmed"},
        {"date": "2026-10-02", "program": "p", "subid": "co-wplay-co", "clicks": "20", "registrations": "1",
         "ftd": "0", "commission_usd": "25", "status": "pending"}])
    md = analytics_report.build(tmp_path)
    assert "| co-wplay-co | 70 | 4 | 1 | 40.00 | 25.00 |" in md
    assert "- CO: 40.00 USD" in md


def test_analytics_without_data(tmp_path):
    assert "Sin datos" in analytics_report.build(tmp_path)


def test_backup_roundtrip_excludes_env(tmp_path, monkeypatch):
    fake_root = tmp_path / "root"
    for d in ("content", "data"):
        (fake_root / d).mkdir(parents=True)
        (fake_root / d / "f.txt").write_text("ok")
    (fake_root / "data" / ".env").write_text("SECRET=1")
    monkeypatch.setattr(backup, "ROOT", fake_root)
    out = backup.create(tmp_path / "bk", keep=2)
    assert backup.verify(out)
    names = tarfile.open(out).getnames()
    assert "data/f.txt" in names and not any(n.endswith(".env") for n in names)
    backup.restore(out, tmp_path / "restored")
    assert (tmp_path / "restored" / "content" / "f.txt").read_text() == "ok"
