# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_doc(filename: str) -> str:
    path = ROOT / filename
    if not path.exists():
        return f"文档 `{filename}` 未找到。"
    return path.read_text(encoding="utf-8")