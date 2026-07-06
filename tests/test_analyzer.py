from core.analyzer import detect_techniques, find_similar, jaccard, load_rules


def test_rules_load(rules):
    assert len(rules) >= 8


def test_detect_techniques():
    found = detect_techniques("为人民服务，团结奋斗")
    techniques = {t["technique"] for t in found}
    assert "情感诉求" in techniques or "牺牲奉献" in techniques or "动员" in techniques


def test_jaccard_identical():
    assert jaccard("共同富裕", "共同富裕") == 1.0


def test_jaccard_different():
    assert jaccard("abc", "xyz") == 0.0


def test_find_similar_order(cases_list):
    results = find_similar("神爱世人永生", cases_list, top_k=5)
    assert len(results) == 5
    scores = [s for _, s in results]
    assert scores == sorted(scores, reverse=True)