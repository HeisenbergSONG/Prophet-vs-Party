# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from core.viz import resolve_chinese_font, term_frequencies, wordcloud_figure

from core.data_loader import load_cases


def test_resolve_chinese_font_returns_existing_path_or_none():
    path = resolve_chinese_font()
    assert path is None or os.path.exists(path)


def test_wordcloud_figure_with_cases():
    df = load_cases().head(10)
    assert term_frequencies(df)
    fig = wordcloud_figure(df)
    if resolve_chinese_font():
        assert fig is not None
    else:
        assert fig is None