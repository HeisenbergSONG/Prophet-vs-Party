# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "cases.json"
MATRIX_PATH = ROOT / "matrix.json"

TYPE_LABELS = {"ccp": "共产党", "christian": "基督教", "islam": "伊斯兰教"}
TYPE_COLORS = {"ccp": "#ef4444", "christian": "#3b82f6", "islam": "#22c55e"}

AUTHOR = "HeisenbergSONG"
REPO_URL = "https://github.com/HeisenbergSONG/Prophet-vs-Party"
APP_URL = "https://prophet-vs-party.streamlit.app"
LICENSE_NAME = "GPL-3.0"
LICENSE_URL = f"{REPO_URL}/blob/main/LICENSE"
ISSUES_URL = f"{REPO_URL}/issues/new"


def cases_data_version() -> str:
    """Change when cases.json updates — busts Streamlit cache on Cloud."""
    stat = CASES_PATH.stat()
    return f"{int(stat.st_mtime)}-{stat.st_size}"


def matrix_data_version() -> str:
    stat = MATRIX_PATH.stat()
    return f"{int(stat.st_mtime)}-{stat.st_size}"


@st.cache_data
def _load_cases_cached(data_version: str) -> pd.DataFrame:
    df = pd.read_json(CASES_PATH)
    df["type_label"] = df["source_type"].map(TYPE_LABELS)
    return df


def load_cases() -> pd.DataFrame:
    return _load_cases_cached(cases_data_version())


@st.cache_data
def _load_matrix_cached(data_version: str) -> dict:
    import json

    with open(MATRIX_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_matrix() -> dict:
    return _load_matrix_cached(matrix_data_version())


def init_session_state():
    if "selected_ids" not in st.session_state:
        st.session_state.selected_ids = []