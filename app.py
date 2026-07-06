# Prophet vs Party — Streamlit MVP
# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import streamlit as st

from core.data_loader import init_session_state, load_cases, load_matrix
from core.viz import matrix_comparison_radar, matrix_table_markup

st.set_page_config(
    page_title="主页",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_home():
    init_session_state()

    st.title("主页")
    st.markdown("**话语之战 · Prophet vs Party** · 中立修辞分析平台")

    st.info(
        "本平台仅供教育与修辞分析，不构成任何价值判断或政治/宗教立场。"
        "用户输入仅在当前会话中分析，**不持久化、不上传第三方**。"
    )

    df = load_cases()
    matrix = load_matrix()
    counts = df["source_type"].value_counts()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("案例总数", len(df))
    col2.metric("共产党", counts.get("ccp", 0))
    col3.metric("基督教", counts.get("christian", 0))
    col4.metric("伊斯兰教", counts.get("islam", 0))

    st.markdown("---")
    st.markdown("### 话术矩阵")
    st.plotly_chart(matrix_comparison_radar(df, matrix), use_container_width=True)
    st.caption("基于各类案例技巧标签在 8 个矩阵维度上的聚合估算，供跨类型修辞轮廓对比。")
    st.markdown(matrix_table_markup(matrix), unsafe_allow_html=True)
    st.caption("矩阵描述各维度典型特征，与 matrix.json 同步。")

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
        st.page_link("pages/5_伦理准则.py", label="伦理准则")
        st.page_link("pages/6_免责声明.py", label="免责声明")
        st.caption("Prophet vs Party · GPLv3")


pages = [
    st.Page(render_home, title="主页", icon="🏠", default=True),
    st.Page("pages/1_案例库.py", title="案例库", icon="📚"),
    st.Page("pages/2_互动分析器.py", title="互动分析器", icon="🔍"),
    st.Page("pages/3_可视化.py", title="可视化", icon="📊"),
    st.Page("pages/4_反馈与贡献.py", title="反馈与贡献", icon="💬"),
    st.Page("pages/5_伦理准则.py", title="伦理准则"),
    st.Page("pages/6_免责声明.py", title="免责声明"),
]

st.navigation(pages).run()