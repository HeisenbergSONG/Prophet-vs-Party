# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import streamlit as st

from core.data_loader import TYPE_LABELS, load_cases, load_matrix
from core.viz import (
    matrix_comparison_radar,
    matrix_table_markup,
    term_frequencies,
    terms_bar_chart,
    timeline_chart,
    wordcloud_figure,
)

st.set_page_config(page_title="可视化", layout="wide")
st.title("📊 可视化")

df = load_cases()
matrix = load_matrix()

tab1, tab2, tab3, tab4 = st.tabs(["时间轴", "词云", "话术矩阵", "分类统计"])

with tab1:
    st.plotly_chart(timeline_chart(df), use_container_width=True)
    st.caption("气泡可悬停查看案例详情；年代为 case 中 year_start/year_end 中点。")

with tab2:
    type_wc = st.selectbox("词云范围", ["全部", "ccp", "christian", "islam"],
                           format_func=lambda x: "全部" if x == "全部" else TYPE_LABELS[x])
    wc_df = df if type_wc == "全部" else df[df["source_type"] == type_wc]
    st.plotly_chart(terms_bar_chart(wc_df), use_container_width=True)
    fig = wordcloud_figure(wc_df)
    if fig:
        st.pyplot(fig)
    elif term_frequencies(wc_df):
        st.warning("未找到支持中文的字体，词云暂无法显示文字。柱状图已展示相同词频数据。")
    else:
        st.caption("当前筛选范围内暂无词频数据。")

with tab3:
    st.plotly_chart(matrix_comparison_radar(df, matrix), use_container_width=True)
    st.caption("基于各类案例技巧标签在 8 个矩阵维度上的聚合估算，供跨类型修辞轮廓对比。")
    st.markdown(matrix_table_markup(matrix), unsafe_allow_html=True)
    st.caption("矩阵描述各维度典型特征，与 matrix.json 同步。")

with tab4:
    by_type = df.groupby("source_type").size().reset_index(name="count")
    by_type["label"] = by_type["source_type"].map(TYPE_LABELS)
    import plotly.express as px
    from core.data_loader import TYPE_COLORS
    fig = px.bar(by_type, x="label", y="count", color="source_type",
                 color_discrete_map=TYPE_COLORS, title="案例类型分布")
    fig2 = px.histogram(df, x="category", color="source_type",
                        color_discrete_map=TYPE_COLORS, title="分类分布")
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)