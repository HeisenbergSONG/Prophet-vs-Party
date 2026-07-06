# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import streamlit as st

LANDSCAPE_HINT_HTML = """
<div id="pnp-landscape-hint" role="status" aria-live="polite">
    <span>📱 移动端竖屏浏览较窄，建议旋转手机<strong>横屏使用</strong>，图表与话术矩阵体验更佳。</span>
</div>
"""

MOBILE_CSS = """
<style>
#pnp-landscape-hint {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999999;
    padding: 0.65rem 1rem;
    padding-top: max(0.65rem, env(safe-area-inset-top));
    background: linear-gradient(90deg, #1e40af, #2563eb);
    color: #fff;
    font-size: 0.85rem;
    line-height: 1.45;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.18);
}
#pnp-landscape-hint strong { font-weight: 700; }

@media (max-width: 768px) and (orientation: portrait) {
    #pnp-landscape-hint {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    [data-testid="stAppViewContainer"] > section.main {
        padding-top: 3.25rem;
    }
}

@supports (padding: max(0px)) {
    .block-container {
        padding-left: max(1rem, env(safe-area-inset-left));
        padding-right: max(1rem, env(safe-area-inset-right));
    }
}

@media (max-width: 768px) {
    .block-container { padding-top: 1rem; padding-bottom: 2rem; }

    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.25rem !important; }
    h3 { font-size: 1.1rem !important; }

    .matrix-wrap {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        margin: 0 -0.25rem;
        padding-bottom: 0.25rem;
    }
    table.matrix { min-width: 36rem; font-size: 0.8rem; }
    table.matrix th, table.matrix td { padding: 0.5rem; }

    div[data-testid="stMetric"] { min-width: 0; }
    div[data-testid="stMetricValue"] { font-size: 1.25rem; }

    .stButton button,
    .stLinkButton a,
    .stDownloadButton button {
        min-height: 2.75rem;
        width: 100%;
    }

    div[data-testid="stTabs"] button { min-height: 2.5rem; font-size: 0.85rem; }

    .stExpander details summary { min-height: 2.75rem; }

    blockquote, p, .stMarkdown { word-break: break-word; overflow-wrap: anywhere; }

    .js-plotly-plot, .js-plotly-plot .plotly { max-width: 100%; }

    div[data-testid="stSidebar"] { min-width: min(18rem, 85vw); }
}
</style>
"""


def inject_mobile_styles() -> None:
    st.markdown(LANDSCAPE_HINT_HTML + MOBILE_CSS, unsafe_allow_html=True)