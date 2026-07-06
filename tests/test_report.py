from core.analyzer import detect_techniques, dimension_scores, find_similar
from core.report import generate_json_report, generate_markdown_report


def test_markdown_report(cases_list, matrix):
    text = "为人民服务"
    tech = detect_techniques(text)
    scores = dimension_scores(tech, matrix)
    similar = find_similar(text, cases_list, top_k=3)
    md = generate_markdown_report(text, tech, scores, similar)
    assert "修辞分析报告" in md
    assert "免责声明" in md or "教育用途" in md


def test_json_report(cases_list, matrix):
    text = "信道者们啊，你们当敬畏真主"
    tech = detect_techniques(text)
    scores = dimension_scores(tech, matrix)
    similar = find_similar(text, cases_list, top_k=2)
    js = generate_json_report(text, tech, scores, similar)
    assert '"query"' in js
    assert "教育用途" in js