# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import json

import streamlit as st

from core.data_loader import ISSUES_URL, TYPE_LABELS, load_cases

st.set_page_config(page_title="反馈与贡献", layout="wide")
st.title("💬 反馈与贡献")

st.markdown("### 报告偏差")
st.markdown(
    "发现引文错误、来源不准或归类不当？请附**可核实的公开来源**，在 GitHub 提交 Issue。"
)
st.link_button("在 GitHub 报告偏差", ISSUES_URL, type="primary")

st.markdown("---")
st.markdown("### 贡献新案例")
st.caption("按 ETHICS.md：公开来源可核实即视为事实，请通过 Pull Request 提交 cases.json 条目。")

df = load_cases()
max_ids = {}
for stype in ["ccp", "christian", "islam"]:
    prefix = stype if stype != "christian" else "christian"
    nums = [int(r.split("_")[1]) for r in df[df["source_type"] == stype]["id"] if "_" in r]
    max_ids[stype] = max(nums) if nums else 0

with st.form("contribute"):
    source_type = st.selectbox("类型", ["ccp", "christian", "islam"], format_func=lambda x: TYPE_LABELS[x])
    text = st.text_input("原文 *")
    source = st.text_input("出处 *")
    source_url = st.text_input("公开来源（文献名/链接）*")
    category = st.text_input("分类", placeholder="如：希望许诺")
    techniques = st.text_input("技巧标签（逗号分隔）", placeholder="希望许诺, 情感诉求")
    mechanism = st.text_input("心理机制")
    era = st.text_input("时代标注", placeholder="如：2020 · 当代")
    year_start = st.number_input("起始年", value=2020, step=1)
    year_end = st.number_input("结束年", value=2026, step=1)
    risk = st.text_input("风险提示（可选）")
    submitted = st.form_submit_button("生成贡献 JSON")

if submitted:
    if not text or not source or not source_url:
        st.error("请填写原文、出处和公开来源")
    else:
        next_n = max_ids[source_type] + 1
        new_case = {
            "id": f"{source_type}_{next_n:03d}",
            "category": category or "待分类",
            "source_type": source_type,
            "text": text,
            "source": source,
            "techniques": [t.strip() for t in techniques.split(",") if t.strip()],
            "psychological_mechanism": mechanism,
            "parallel": {},
            "tags": ["贡献"],
            "risk_note": risk,
            "source_url": source_url,
            "year_start": int(year_start),
            "year_end": int(year_end),
            "era": era or f"{year_start}-{year_end}",
        }
        st.success("请复制以下 JSON，追加到 cases.json 后发起 Pull Request：")
        st.code(json.dumps(new_case, ensure_ascii=False, indent=2), language="json")

st.markdown("---")
st.markdown("### 隐私说明")
st.info("本应用不收集用户输入的持久化数据。反馈通过 GitHub Issues 公开处理。")