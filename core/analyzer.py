# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import re
from pathlib import Path

import numpy as np
import streamlit as st
import yaml

ROOT = Path(__file__).resolve().parent.parent


@st.cache_data
def load_rules() -> list[dict]:
    with open(ROOT / "rules.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    rules = []
    for r in data["rules"]:
        rules.append({
            "pattern": re.compile(r["pattern"]),
            "technique": r["technique"],
            "dim": r["dim"],
        })
    return rules


def bigrams(text: str) -> set[str]:
    s = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", text)
    return {s[i : i + 2] for i in range(len(s) - 1)} if len(s) > 1 else set()


def jaccard(a: str, b: str) -> float:
    A, B = bigrams(a), bigrams(b)
    if not A and not B:
        return 0.0
    inter = len(A & B)
    union = len(A | B)
    return inter / union if union else 0.0


def detect_techniques(text: str) -> list[dict]:
    found = []
    seen = set()
    for rule in load_rules():
        if rule["pattern"].search(text):
            key = rule["technique"]
            if key not in seen:
                seen.add(key)
                found.append(rule)
    return found


def dimension_scores(techniques: list[dict], matrix: dict) -> dict[str, float]:
    dims = {d["key"]: 20.0 for d in matrix["dimensions"]}
    dim_keys = {d["key"] for d in matrix["dimensions"]}
    for t in techniques:
        if t["dim"] in dim_keys:
            dims[t["dim"]] = min(dims.get(t["dim"], 20) + 35, 100)
    label_map = {d["key"]: d["label"] for d in matrix["dimensions"]}
    return {label_map[k]: v for k, v in dims.items()}


def score_case_techniques(case_techniques: list[str], matrix: dict) -> dict[str, float]:
    dims = {d["key"]: 20.0 for d in matrix["dimensions"]}
    for dim in matrix["dimensions"]:
        overlap = set(case_techniques) & set(dim["techniques"])
        if overlap:
            dims[dim["key"]] = min(60 + len(overlap) * 15, 100)
    label_map = {d["key"]: d["label"] for d in matrix["dimensions"]}
    return {label_map[k]: v for k, v in dims.items()}


@st.cache_resource
def load_embedding_model():
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    except Exception:
        return None


@st.cache_data
def compute_case_embeddings(texts: tuple[str, ...]) -> np.ndarray | None:
    model = load_embedding_model()
    if model is None:
        return None
    return model.encode(list(texts), show_progress_bar=False)


def hybrid_similarity(query: str, case: dict, emb_query: np.ndarray | None, emb_cases: np.ndarray | None, idx: int) -> float:
    tech_text = " ".join(case.get("techniques", []))
    j_score = jaccard(query, case["text"]) * 0.6 + jaccard(query, tech_text) * 0.4
    if emb_query is not None and emb_cases is not None:
        from numpy.linalg import norm

        a, b = emb_query, emb_cases[idx]
        cos = float(np.dot(a, b) / (norm(a) * norm(b) + 1e-9))
        return 0.6 * cos + 0.4 * j_score
    return j_score


def find_similar(query: str, cases: list[dict], top_k: int = 5) -> list[tuple[dict, float]]:
    texts = tuple(c["text"] for c in cases)
    emb_cases = compute_case_embeddings(texts)
    emb_query = None
    if emb_cases is not None:
        model = load_embedding_model()
        if model is not None:
            emb_query = model.encode(query, show_progress_bar=False)

    scored = []
    for i, case in enumerate(cases):
        s = hybrid_similarity(query, case, emb_query, emb_cases, i)
        scored.append((case, s))
    scored.sort(key=lambda x: -x[1])
    return scored[:top_k]


def mixed_discourse_recommend(query: str, cases: list[dict]) -> dict[str, tuple[dict, float]]:
    similar = find_similar(query, cases, top_k=30)
    result = {}
    for case, score in similar:
        stype = case["source_type"]
        if stype not in result:
            result[stype] = (case, score)
        if len(result) == 3:
            break
    return result