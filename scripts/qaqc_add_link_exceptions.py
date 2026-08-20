#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCEPTIONS = ROOT / "data" / "link_role_exceptions.json"

NEW = [
    {
        "resource_id": "DR0004",
        "rationale": "A página oficial do SIRENE é simultaneamente a apresentação institucional do sistema e o ponto de acesso aos resultados, publicações, dados e ferramentas de emissões. O MCTI documenta o SIRENE como plataforma oficial de disponibilização e transparência dos dados nacionais de GEE; manter a mesma URL é deliberado no nível da fonte.",
        "evidence_url": "https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene",
        "reviewed_at": "2026-08-19",
    },
    {
        "resource_id": "DR0133",
        "rationale": "O IpeaData é um catálogo/serviço de séries em que a página principal funciona como a própria interface pública de navegação, seleção e acesso às séries. Como a fonte representa o serviço federado, não existe um único dataset alternativo que deva substituir a landing page como data_access_url.",
        "evidence_url": "https://www.ipeadata.gov.br/Default.aspx",
        "reviewed_at": "2026-08-19",
    },
]

payload = json.loads(EXCEPTIONS.read_text(encoding="utf-8"))
items = payload.setdefault("reviewed_same_destination", [])
existing = {item["resource_id"] for item in items}
for item in NEW:
    if item["resource_id"] not in existing:
        items.append(item)
EXCEPTIONS.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

subprocess.run(["python3", "scripts/audit_link_roles.py", "--write"], cwd=ROOT, check=True)
