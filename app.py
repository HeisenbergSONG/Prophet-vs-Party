# Prophet vs Party — Streamlit MVP
# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import streamlit as st

from core.data_loader import init_session_state, load_cases

st.set_page_config(
    page_title="话语之战",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()

st.title("话语之战 · Prophet vs Party")
st.markdown("**宣传 vs 传教** · 中立修辞分析平台")

st.info(
    "本平台仅供教育与修辞分析，不构成任何价值判断或政治/宗教立场。"
    "用户输入仅在当前会话中分析，**不持久化、不上传第三方**。"
)

df = load_cases()
counts = df["source_type"].value_counts()

col1, col2, col3, col4 = st.columns(4)
col1.metric("案例总数", len(df))
col2.metric("共产党", counts.get("ccp", 0))
col3.metric("基督教", counts.get("christian", 0))
col4.metric("伊斯兰教", counts.get("islam", 0))

st.markdown("---")
st.markdown("### 快速导航")
st.markdown("""
- **📚 案例库** — 搜索、筛选、选择 2–3 条案例对比
- **🔍 互动分析器** — 输入文本，检测修辞技巧与相似案例
- **📊 可视化** — 时间轴、词云、话术矩阵、相似度热力图
- **💬 反馈与贡献** — 报告偏差、生成案例贡献模板
""")

with st.sidebar:
    st.markdown("### 文档")
    st.markdown("[伦理准则](ETHICS.md) · [免责声明](DISCLAIMER.md)")
    st.markdown("### 其他入口")
    st.markdown("[HTML 静态原型](index_test.html)")
    st.caption("Prophet vs Party · GPLv3")