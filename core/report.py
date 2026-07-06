# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from datetime import datetime

import numpy as np

from core.data_loader import TYPE_LABELS


def _sanitize(obj):
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    return obj


def generate_markdown_report(
    query: str,
    techniques: list[dict],
    scores: dict[str, float],
    similar: list[tuple[dict, float]],
    mixed: dict | None = None,
) -> str:
    lines = [
        "# 话语之战 · 修辞分析报告",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "> 教育用途，不构成价值判断。",
        "",
        f"## 分析文本\n\n{query}",
        "",
        "## 检测到的技巧",
    ]
    if techniques:
        for t in techniques:
            lines.append(f"- **{t['technique']}**（维度：{t['dim']}）")
    else:
        lines.append("- 未匹配到预设规则")

    lines.append("")
    lines.append("## 维度评分（启发式估算）")
    for label, val in scores.items():
        if val > 20:
            lines.append(f"- {label}：{val:.0f}")

    lines.append("")
    lines.append("## 相似案例")
    for case, score in similar:
        lines.append(f"### {TYPE_LABELS[case['source_type']]} · {case['category']}")
        lines.append(f"- 文本：{case['text']}")
        lines.append(f"- 来源：{case['source']} · {case.get('era', '')}")
        lines.append(f"- 数据：{case.get('source_url', '')}")
        lines.append(f"- 相似度：{score:.0%}")
        lines.append("")

    if mixed:
        lines.append("## 混合话术参考（三类各一条）")
        for stype, (case, score) in mixed.items():
            lines.append(f"- **{TYPE_LABELS[stype]}**：{case['text']}（{score:.0%}）")

    return "\n".join(lines)


def generate_json_report(
    query: str,
    techniques: list[dict],
    scores: dict[str, float],
    similar: list[tuple[dict, float]],
    mixed: dict | None = None,
) -> str:
    payload = {
        "generated": datetime.now().isoformat(),
        "disclaimer": "教育用途，不构成价值判断",
        "query": query,
        "techniques": [{"technique": t["technique"], "dim": t["dim"]} for t in techniques],
        "dimension_scores": scores,
        "similar_cases": [
            {"case": _sanitize(c), "score": round(float(s), 4)} for c, s in similar
        ],
    }
    if mixed:
        payload["mixed_discourse"] = {
            k: {"case": _sanitize(v[0]), "score": round(float(v[1]), 4)} for k, v in mixed.items()
        }
    return json.dumps(_sanitize(payload), ensure_ascii=False, indent=2)