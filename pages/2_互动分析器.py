# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import streamlit as st

from core.analyzer import (
    detect_techniques,
    dimension_scores,
    find_similar,
    load_embedding_model,
    mixed_discourse_recommend,
)
from core.data_loader import TYPE_LABELS, load_cases, load_matrix
from core.source_utils import format_source_html
from core.report import generate_json_report, generate_markdown_report
from core.viz import radar_chart, similarity_heatmap

st.set_page_config(page_title="互动分析器", layout="wide")
st.title("🔍 互动分析器")

st.caption("输入文本仅在当前会话分析，不持久化。")

cases = load_cases().to_dict("records")
matrix = load_matrix()

model = load_embedding_model()
if model:
    st.success("语义相似度模型已加载（sentence-transformers + Jaccard 混合）")
else:
    st.warning("语义模型未加载，使用 Jaccard 相似度（仍可正常使用）")

text = st.text_area("输入待分析文本", height=120, placeholder="粘贴或输入一段宣传/传教话术…")

if st.button("分析", type="primary", use_container_width=True) and text.strip():
    techniques = detect_techniques(text)
    scores = dimension_scores(techniques, matrix)
    similar = find_similar(text, cases, top_k=8)
    mixed = mixed_discourse_recommend(text, cases)

    st.session_state.last_analysis = {
        "text": text,
        "techniques": techniques,
        "scores": scores,
        "similar": similar,
        "mixed": mixed,
    }

if "last_analysis" in st.session_state:
    a = st.session_state.last_analysis
    st.markdown("### 检测到的技巧")
    if a["techniques"]:
        st.write(", ".join(f"**{t['technique']}**" for t in a["techniques"]))
    else:
        st.write("未匹配到预设规则")

    st.markdown("### 维度评分")
    st.plotly_chart(
        radar_chart([a["scores"]], ["当前输入"]),
        use_container_width=True,
    )

    st.markdown("### 相似案例")
    sim_cases = [c for c, _ in a["similar"]]
    sim_scores = [s for _, s in a["similar"]]
    st.plotly_chart(similarity_heatmap(a["text"], sim_cases, sim_scores), use_container_width=True)

    for case, score in a["similar"][:5]:
        with st.container(border=True):
            st.markdown(f"**{TYPE_LABELS[case['source_type']]}** · {case['category']} · 相似度 **{score:.0%}**")
            st.markdown(f"> {case['text']}")
            st.markdown(
                f"<p style='font-size:0.8rem;color:gray'>{case['source']} · {format_source_html(case)}</p>",
                unsafe_allow_html=True,
            )

    st.markdown("### 混合话术实验")
    st.caption("三类话语各推荐一条修辞结构相似的案例，仅供对照，非立场等效。")
    for stype, (case, score) in a["mixed"].items():
        with st.container(border=True):
            st.markdown(f"**{TYPE_LABELS[stype]}** ({score:.0%})")
            st.markdown(f"> {case['text']}")

    md = generate_markdown_report(a["text"], a["techniques"], a["scores"], a["similar"], a["mixed"])
    js = generate_json_report(a["text"], a["techniques"], a["scores"], a["similar"], a["mixed"])
    st.download_button("下载 Markdown 报告", md, "report.md", "text/markdown", use_container_width=True)
    st.download_button("下载 JSON 报告", js, "report.json", "application/json", use_container_width=True)