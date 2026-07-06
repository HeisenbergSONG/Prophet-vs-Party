# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import streamlit as st

from core.doc_loader import read_doc

st.set_page_config(page_title="免责声明", layout="wide")
st.markdown(read_doc("DISCLAIMER.md"))