# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from pathlib import Path

from core.case_schema import validate_case

ROOT = Path(__file__).resolve().parent.parent


def test_sample_standard_valid():
    sample = json.loads((ROOT / "sample_standard.json").read_text(encoding="utf-8"))
    assert validate_case(sample) == []


def test_validate_case_detects_missing_link():
    bad = {
        "id": "ccp_999",
        "source_type": "ccp",
        "text": "测试",
        "source": "测试",
        "source_url": "描述",
        "techniques": ["希望许诺"],
        "year_start": 2020,
        "year_end": 2026,
        "era": "2020",
        "source_type_ref": "link",
        "source_verified": False,
    }
    assert any("source_link" in e for e in validate_case(bad))