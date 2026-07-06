import json
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def cases_df() -> pd.DataFrame:
    return pd.read_json(ROOT / "cases.json")


@pytest.fixture
def cases_list(cases_df) -> list[dict]:
    return cases_df.to_dict("records")


@pytest.fixture
def matrix() -> dict:
    with open(ROOT / "matrix.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def rules() -> list:
    import yaml

    with open(ROOT / "rules.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)["rules"]