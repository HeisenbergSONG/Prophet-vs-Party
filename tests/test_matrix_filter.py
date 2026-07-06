# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

from core.data_loader import load_cases, load_matrix
from core.matrix_filter import filter_by_dimension, get_dimension, suggest_case_for_type


def test_get_dimension_by_key(matrix):
    dim = get_dimension(matrix, "emotion")
    assert dim is not None
    assert dim["label"] == "情感诉求"


def test_filter_by_dimension_returns_subset(cases_df, matrix):
    result = filter_by_dimension(cases_df, matrix, "emotion")
    assert len(result) > 0
    assert len(result) <= len(cases_df)
    for _, row in result.iterrows():
        assert set(row["techniques"]) & set(get_dimension(matrix, "emotion")["techniques"])


def test_suggest_case_per_type(cases_df, matrix):
    for stype in ("ccp", "christian", "islam"):
        case = suggest_case_for_type(cases_df, matrix, "future", stype)
        if case:
            assert case["source_type"] == stype