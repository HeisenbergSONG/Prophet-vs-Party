# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

from core.source_utils import VALID_REF_TYPES

REQUIRED_FIELDS = {
    "id", "source_type", "text", "source", "source_url",
    "techniques", "year_start", "year_end", "era",
    "source_type_ref", "source_verified",
}

VALID_SOURCE_TYPES = {"ccp", "christian", "islam"}


def validate_case(case: dict) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_FIELDS - set(case.keys())
    if missing:
        errors.append(f"缺少字段：{', '.join(sorted(missing))}")

    if case.get("source_type") not in VALID_SOURCE_TYPES:
        errors.append("source_type 须为 ccp / christian / islam")

    if case.get("source_type_ref") not in VALID_REF_TYPES:
        errors.append("source_type_ref 须为 link / citation / archive")

    if not case.get("source_url"):
        errors.append("source_url 不能为空")

    if case.get("source_type_ref") == "link":
        link = case.get("source_link")
        if not link or not str(link).startswith("http"):
            errors.append("source_type_ref=link 时须提供 http(s) source_link")

    ys, ye = case.get("year_start"), case.get("year_end")
    if ys is not None and ye is not None and ys > ye:
        errors.append("year_start 不能大于 year_end")

    techs = case.get("techniques")
    if not techs or not isinstance(techs, list):
        errors.append("techniques 须为非空列表")

    return errors