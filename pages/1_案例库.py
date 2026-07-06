# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import streamlit as st

from core.analyzer import score_case_techniques
from core.data_loader import REPO_URL, TYPE_LABELS, init_session_state, load_cases, load_matrix
from core.matrix_filter import dimension_options, filter_by_dimension, suggest_case_for_type
from core.source_utils import format_source_html
from core.viz import radar_chart

st.set_page_config(page_title="案例库", layout="wide")
init_session_state()

st.title("📚 案例库")
df = load_cases()
matrix = load_matrix()
dim_map = dict(dimension_options(matrix))

with st.expander("话术矩阵筛选", expanded=False):
    st.caption("按 8 维矩阵匹配技巧标签；可为共产党 / 基督教 / 伊斯兰教各推荐一条加入对比。")
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        matrix_dim = st.selectbox(
            "矩阵维度",
            [""] + list(dim_map.keys()),
            format_func=lambda k: "不限" if not k else dim_map[k],
            key="matrix_dim_select",
        )
    with mcol2:
        matrix_type = st.selectbox(
            "类型",
            ["", "ccp", "christian", "islam"],
            format_func=lambda x: "全部" if not x else TYPE_LABELS[x],
            key="matrix_type_select",
        )
    if matrix_dim and st.button("三类各推荐 1 条并加入对比", use_container_width=True):
        added = 0
        for stype in ("ccp", "christian", "islam"):
            if len(st.session_state.selected_ids) >= 3:
                break
            case = suggest_case_for_type(df, matrix, matrix_dim, stype)
            if case and case["id"] not in st.session_state.selected_ids:
                st.session_state.selected_ids.append(case["id"])
                added += 1
        if added:
            st.toast(f"已加入 {added} 条")
            st.rerun()
        else:
            st.warning("未找到可推荐案例，或对比栏已满（最多 3 条）。")

query = st.text_input("搜索", placeholder="关键词、来源、技巧…")
type_filter = st.selectbox(
    "类型", ["", "ccp", "christian", "islam"],
    format_func=lambda x: "全部" if not x else TYPE_LABELS[x],
)
cat_filter = st.selectbox("分类", [""] + sorted(df["category"].unique()))

filtered = df.copy()
if matrix_dim:
    filtered = filter_by_dimension(
        filtered, matrix, matrix_dim,
        source_type=matrix_type or None,
    )
if query:
    mask = filtered.apply(
        lambda r: query.lower() in " ".join([
            str(r["text"]), str(r["source"]), str(r["category"]),
            str(r.get("era", "")), " ".join(r.get("techniques", []) or []),
        ]).lower(),
        axis=1,
    )
    filtered = filtered[mask]
if type_filter:
    filtered = filtered[filtered["source_type"] == type_filter]
if cat_filter:
    filtered = filtered[filtered["category"] == cat_filter]

if matrix_dim:
    st.caption(f"矩阵筛选：**{dim_map[matrix_dim]}** · 显示 {len(filtered)} / {len(df)} 条")
else:
    st.caption(f"显示 {len(filtered)} / {len(df)} 条")

if st.session_state.selected_ids:
    selected_df = df[df["id"].isin(st.session_state.selected_ids)]
    with st.container(border=True):
        st.subheader(f"已选对比（{len(st.session_state.selected_ids)} 条）")
        if st.button("清空选择", key="clear_selection_top", use_container_width=True):
            st.session_state.selected_ids = []
            st.rerun()
        if len(st.session_state.selected_ids) >= 2:
            scores_list = []
            labels = []
            for _, row in selected_df.iterrows():
                scores_list.append(score_case_techniques(list(row.get("techniques", []) or []), matrix))
                labels.append(f"{row['type_label']}：{row['text'][:10]}…")
            st.markdown("#### 8 维修辞对比")
            st.plotly_chart(radar_chart(scores_list, labels), use_container_width=True)
            for _, row in selected_df.iterrows():
                with st.expander(f"{row['type_label']} · {row['text'][:20]}…"):
                    st.markdown(f"**{row['text']}**")
                    st.write("来源：", row["source"])
                    if row.get("parallel"):
                        st.markdown("**平行映射**")
                        for k, v in row["parallel"].items():
                            st.write(f"- {TYPE_LABELS.get(k, k)}：{v}")
        else:
            st.info("再选 1 条案例即可生成 8 维雷达对比图。")
        st.markdown(" ".join(f"`{row['id']}`" for _, row in selected_df.iterrows()))

for _, row in filtered.iterrows():
    cid = row["id"]
    selected = cid in st.session_state.selected_ids
    with st.container(border=True):
        st.markdown(f"**{row['type_label']}** · {row['category']} · _{row.get('era', '')}_")
        st.markdown(f"> {row['text']}")
        st.markdown(
            f"<p style='font-size:0.8rem;color:gray'>来源：{row['source']} · 数据：{format_source_html(row.to_dict())}</p>",
            unsafe_allow_html=True,
        )
        techs = row.get("techniques", []) or []
        st.markdown(" ".join(f"`{t}`" for t in techs))
        with st.expander("详情"):
            st.write("心理机制：", row.get("psychological_mechanism", ""))
            if row.get("parallel"):
                st.json(row["parallel"])
            if row.get("risk_note"):
                st.warning(row["risk_note"])
        label = "取消对比" if selected else "加入对比"
        btn_type = "primary" if not selected else "secondary"
        if st.button(label, key=f"sel_{cid}", use_container_width=True, type=btn_type):
            if selected:
                st.session_state.selected_ids.remove(cid)
            elif len(st.session_state.selected_ids) < 3:
                st.session_state.selected_ids.append(cid)
            else:
                st.toast("最多选择 3 条")
            st.rerun()