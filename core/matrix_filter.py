# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import pandas as pd


def get_dimension(matrix: dict, dim_key: str) -> dict | None:
    for dim in matrix["dimensions"]:
        if dim["key"] == dim_key or dim["label"] == dim_key:
            return dim
    return None


def dimension_options(matrix: dict) -> list[tuple[str, str]]:
    return [(d["key"], d["label"]) for d in matrix["dimensions"]]


def filter_by_dimension(
    df: pd.DataFrame,
    matrix: dict,
    dim_key: str,
    *,
    source_type: str | None = None,
) -> pd.DataFrame:
    dim = get_dimension(matrix, dim_key)
    if not dim:
        return df.iloc[0:0]
    techs = set(dim["techniques"])
    if not techs:
        return df.iloc[0:0]

    def matches(row) -> bool:
        row_techs = set(row.get("techniques") or [])
        if not row_techs & techs:
            return False
        if source_type and row.get("source_type") != source_type:
            return False
        return True

    return df[df.apply(matches, axis=1)]


def suggest_case_for_type(df: pd.DataFrame, matrix: dict, dim_key: str, source_type: str) -> dict | None:
    subset = filter_by_dimension(df, matrix, dim_key, source_type=source_type)
    if subset.empty:
        return None
    return subset.iloc[0].to_dict()