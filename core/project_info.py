# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import streamlit as st

from core.data_loader import APP_URL, AUTHOR, ISSUES_URL, LICENSE_NAME, LICENSE_URL, REPO_URL


def render_project_sidebar() -> None:
    st.markdown("### 项目")
    st.caption(f"作者：[{AUTHOR}](https://github.com/{AUTHOR})")
    st.link_button("GitHub 仓库", REPO_URL, use_container_width=True)
    st.link_button("在线应用", APP_URL, use_container_width=True)
    st.markdown("---")
    st.markdown("### 文档")
    st.page_link("pages/5_伦理准则.py", label="伦理准则")
    st.page_link("pages/6_免责声明.py", label="免责声明")
    st.link_button("报告问题", ISSUES_URL, use_container_width=True)
    st.markdown("---")
    st.caption(f"Prophet vs Party · [{LICENSE_NAME}]({LICENSE_URL})")


def render_project_footer() -> None:
    st.markdown("---")
    st.caption(
        f"**话语之战**（Prophet vs Party）· 作者 [{AUTHOR}](https://github.com/{AUTHOR}) "
        f"· [GitHub 仓库]({REPO_URL}) · [在线应用]({APP_URL}) · [{LICENSE_NAME}]({LICENSE_URL})"
    )