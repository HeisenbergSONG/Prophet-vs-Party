# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import streamlit as st

MOBILE_CSS = """
<style>
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
    st.markdown(MOBILE_CSS, unsafe_allow_html=True)