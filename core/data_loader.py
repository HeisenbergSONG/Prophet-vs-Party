# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent

TYPE_LABELS = {"ccp": "共产党", "christian": "基督教", "islam": "伊斯兰教"}
TYPE_COLORS = {"ccp": "#ef4444", "christian": "#3b82f6", "islam": "#22c55e"}

AUTHOR = "HeisenbergSONG"
REPO_URL = "https://github.com/HeisenbergSONG/Prophet-vs-Party"
APP_URL = "https://prophet-vs-party.streamlit.app"
LICENSE_NAME = "GPL-3.0"
LICENSE_URL = f"{REPO_URL}/blob/main/LICENSE"
ISSUES_URL = f"{REPO_URL}/issues/new"


@st.cache_data
def load_cases() -> pd.DataFrame:
    df = pd.read_json(ROOT / "cases.json")
    df["type_label"] = df["source_type"].map(TYPE_LABELS)
    return df


@st.cache_data
def load_matrix() -> dict:
    import json

    with open(ROOT / "matrix.json", encoding="utf-8") as f:
        return json.load(f)


def init_session_state():
    if "selected_ids" not in st.session_state:
        st.session_state.selected_ids = []