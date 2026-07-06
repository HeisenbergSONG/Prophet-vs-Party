# Copyright (C) 2026 HeisenbergSONG
# SPDX-License-Identifier: GPL-3.0-or-later

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from core.data_loader import TYPE_COLORS, TYPE_LABELS


def radar_chart(scores_list: list[dict[str, float]], labels: list[str]) -> go.Figure:
    categories = list(scores_list[0].keys()) if scores_list else []
    fig = go.Figure()
    colors = ["#ef4444", "#3b82f6", "#22c55e", "#a855f7"]
    for i, (scores, label) in enumerate(zip(scores_list, labels)):
        vals = [scores.get(c, 20) for c in categories]
        vals.append(vals[0])
        cats = categories + [categories[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats, fill="toself", name=label,
            line_color=colors[i % len(colors)],
            opacity=0.6,
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True, height=450,
    )
    return fig


def matrix_comparison_radar(df: pd.DataFrame, matrix: dict) -> go.Figure:
    from core.analyzer import score_case_techniques

    scores_list = []
    labels = []
    for stype in ("ccp", "christian", "islam"):
        subset = df[df["source_type"] == stype]
        techs: list[str] = []
        for row_techs in subset["techniques"]:
            techs.extend(row_techs or [])
        scores_list.append(score_case_techniques(techs, matrix))
        labels.append(TYPE_LABELS[stype])
    fig = radar_chart(scores_list, labels)
    fig.update_layout(title="8 维话术矩阵对比")
    return fig


def timeline_chart(df: pd.DataFrame) -> go.Figure:
    plot_df = df.copy()
    plot_df["mid_year"] = (plot_df["year_start"] + plot_df["year_end"]) / 2
    fig = px.scatter(
        plot_df, x="mid_year", y="source_type", color="source_type",
        color_discrete_map=TYPE_COLORS,
        hover_data=["text", "era", "category"],
        labels={"mid_year": "年代", "source_type": "类型"},
        title="话术历史分布",
    )
    fig.update_yaxes(tickvals=["ccp", "christian", "islam"], ticktext=list(TYPE_LABELS.values()))
    return fig


def similarity_heatmap(query: str, cases: list[dict], scores: list[float]) -> go.Figure:
    labels = [f"{TYPE_LABELS[c['source_type']][:2]}·{c['text'][:8]}…" for c in cases]
    fig = go.Figure(data=go.Heatmap(
        z=[scores],
        x=labels,
        y=["相似度"],
        colorscale="Blues",
        text=[[f"{s:.0%}" for s in scores]],
        texttemplate="%{text}",
        textfont={"size": 10},
    ))
    fig.update_layout(title=f"与「{query[:20]}…」的相似度", height=200)
    return fig


def term_frequencies(df: pd.DataFrame) -> dict[str, int]:
    from collections import Counter

    freq: Counter = Counter()
    for _, row in df.iterrows():
        for t in row.get("techniques", []) or []:
            freq[str(t)] += 3
        for tag in row.get("tags", []) or []:
            freq[str(tag)] += 2
        text = str(row["text"])
        clean = "".join(c for c in text if "\u4e00" <= c <= "\u9fff")
        for i in range(len(clean) - 1):
            freq[clean[i : i + 2]] += 1
    return dict(freq.most_common(40))


def terms_bar_chart(df: pd.DataFrame) -> go.Figure:
    freq = term_frequencies(df)
    if not freq:
        return go.Figure()
    items = list(freq.items())
    fig = go.Figure(go.Bar(
        x=[v for _, v in items], y=[k for k, _ in items],
        orientation="h",
    ))
    fig.update_layout(title="高频修辞词/技巧", height=500, yaxis=dict(autorange="reversed"))
    return fig


def resolve_chinese_font() -> str | None:
    import os

    import matplotlib.font_manager as fm

    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/NotoSansSC-VF.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansSC-Regular.otf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path

    keywords = (
        "noto sans sc", "noto sans cjk sc", "source han sans sc",
        "wqy zenhei", "wqy microhei", "wenquanyi zen hei",
        "microsoft yahei", "simhei", "simsun", "pingfang sc",
    )
    for font in fm.fontManager.ttflist:
        name = font.name.lower()
        if any(k in name for k in keywords):
            return font.fname
    return None


def wordcloud_figure(df: pd.DataFrame):
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    freq = term_frequencies(df)
    if not freq:
        return None

    font_path = resolve_chinese_font()
    if not font_path:
        return None

    wc = WordCloud(
        width=800, height=400, background_color="white",
        font_path=font_path, max_words=80,
    ).generate_from_frequencies(freq)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    plt.tight_layout()
    return fig


def matrix_table_html(matrix: dict) -> str:
    rows = []
    for dim in matrix["dimensions"]:
        rows.append(
            f"<tr><td class='dim'>{dim['label']}</td>"
            f"<td>{dim['ccp']}</td><td>{dim['christian']}</td><td>{dim['islam']}</td></tr>"
        )
    return (
        "<table class='matrix'><thead><tr><th>维度</th><th>共产党</th><th>基督教</th><th>伊斯兰教</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )