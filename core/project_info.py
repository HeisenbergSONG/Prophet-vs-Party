# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import streamlit as st

from core.data_loader import (
    APP_URL,
    AUTHOR,
    ISSUES_URL,
    LICENSE_NAME,
    LICENSE_URL,
    REPO_URL,
    cases_data_version,
    load_cases,
)


def render_project_sidebar(*, ethics_page=None, disclaimer_page=None) -> None:
    st.markdown("### 项目")
    st.caption(f"作者：[{AUTHOR}](https://github.com/{AUTHOR})")
    st.link_button("GitHub 仓库", REPO_URL, use_container_width=True)
    st.link_button("在线应用", APP_URL, use_container_width=True)
    st.markdown("---")
    st.markdown("### 文档")
    if ethics_page is not None:
        st.page_link(ethics_page, label="伦理准则")
    else:
        st.markdown("[伦理准则](/ethics)")
    if disclaimer_page is not None:
        st.page_link(disclaimer_page, label="免责声明")
    else:
        st.markdown("[免责声明](/disclaimer)")
    st.link_button("报告问题", ISSUES_URL, use_container_width=True)
    st.markdown("---")
    try:
        n = len(load_cases())
        st.caption(f"案例库 · {n} 条 · v{cases_data_version()}")
    except OSError:
        pass
    st.caption(f"Prophet vs Party · [{LICENSE_NAME}]({LICENSE_URL})")


def render_project_footer() -> None:
    st.markdown("---")
    st.caption(
        f"**话语之战**（Prophet vs Party）· 作者 [{AUTHOR}](https://github.com/{AUTHOR}) "
        f"· [GitHub 仓库]({REPO_URL}) · [在线应用]({APP_URL}) · [{LICENSE_NAME}]({LICENSE_URL})"
    )