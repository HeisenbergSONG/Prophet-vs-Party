# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

from html import escape

VALID_REF_TYPES = {"link", "citation", "archive"}


def format_source_markdown(case: dict) -> str:
    label = case.get("source_url") or case.get("source") or "未标注"
    link = case.get("source_link")
    if link and str(link).startswith("http"):
        return f"[{label}]({link})"
    ref_type = case.get("source_type_ref", "citation")
    return f"{label}（{ref_type}）"


def format_source_html(case: dict) -> str:
    label = escape(case.get("source_url") or case.get("source") or "未标注")
    link = case.get("source_link")
    if link and str(link).startswith("http"):
        return f'<a href="{escape(str(link))}" target="_blank" rel="noopener">{label}</a>'
    return label