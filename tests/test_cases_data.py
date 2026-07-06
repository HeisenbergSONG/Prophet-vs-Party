from core.source_utils import VALID_REF_TYPES

REQUIRED_COLUMNS = {
    "id", "source_type", "text", "source", "source_url",
    "techniques", "year_start", "year_end", "era",
    "source_type_ref", "source_verified",
}


def test_cases_count_and_balance(cases_df):
    assert len(cases_df) == 60
    counts = cases_df["source_type"].value_counts().to_dict()
    assert counts == {"ccp": 20, "christian": 20, "islam": 20}


def test_required_columns(cases_df):
    assert REQUIRED_COLUMNS.issubset(set(cases_df.columns))


def test_unique_ids(cases_df):
    assert cases_df["id"].is_unique


def test_year_range(cases_df):
    assert (cases_df["year_start"] <= cases_df["year_end"]).all()


def test_source_ref_types(cases_df):
    for _, row in cases_df.iterrows():
        assert row["source_type_ref"] in VALID_REF_TYPES
        assert bool(row["source_url"])
        if row["source_type_ref"] == "link":
            link = row.get("source_link")
            assert link and str(link).startswith("http"), row["id"]


def test_majority_have_links(cases_df):
    linked = cases_df["source_link"].notna() & cases_df["source_link"].astype(str).str.startswith("http")
    assert linked.sum() >= 40