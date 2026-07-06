# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from core.viz import matrix_comparison_radar, resolve_chinese_font, term_frequencies, wordcloud_figure

from core.data_loader import load_cases, load_matrix


def test_resolve_chinese_font_returns_existing_path_or_none():
    path = resolve_chinese_font()
    assert path is None or os.path.exists(path)


def test_matrix_comparison_radar_has_eight_axes():
    df = load_cases()
    matrix = load_matrix()
    fig = matrix_comparison_radar(df, matrix)
    assert len(fig.data) == 3
    assert len(fig.data[0].theta) == 9  # 8 dimensions + closing point


def test_wordcloud_figure_with_cases():
    df = load_cases().head(10)
    assert term_frequencies(df)
    fig = wordcloud_figure(df)
    if resolve_chinese_font():
        assert fig is not None
    else:
        assert fig is None