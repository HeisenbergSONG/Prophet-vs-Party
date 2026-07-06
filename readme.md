# 程序设计方案：宣传 vs 传教对比分析平台

**名称**：  
**Prophet vs Party**（先知 vs 政党）  
或中文名：**「话语之战」——共产党宣传与宗教传教对比分析平台**

**在线演示**（公开）：https://prophet-vs-party.streamlit.app
**源码仓库**：https://github.com/HeisenbergSONG/Prophet-vs-Party  
**作者**：[HeisenbergSONG](https://github.com/HeisenbergSONG) · **协议**：[GPLv3](./LICENSE)

## 定位

一个**中立、教育性**的交互式工具，帮助用户系统地对比**共产党（以中共为代表）宣传话术**与**基督教、伊斯兰教传教话术**的异同。  
核心目标是**分析修辞技巧、心理机制、动员策略**，而非评判优劣。

## 三分钟上手

1. 打开 [在线应用](https://prophet-vs-party.streamlit.app) → **案例库**
2. 展开 **话术矩阵筛选**，选维度后点「三类各推荐 1 条并加入对比」，或手动点「加入对比」（2–3 条）
3. 查看顶部 **8 维修辞对比** 雷达图；或在 **互动分析器** 输入文本 → 导出 Markdown/JSON 报告

## 当前进度（2026-07）

| 阶段 | 状态 | 说明 |
|------|------|------|
| 阶段 0–1 | ✅ | 伦理文档、60 平衡案例、HTML 静态原型 |
| 阶段 2 | ✅ | Streamlit 多页面 MVP |
| 阶段 2.5 | ✅ | Streamlit Cloud 公开部署、移动端优化、线上问题修复 |
| 阶段 4.5 | 🟡 | 零成本运营：贡献流程、矩阵筛选、案例扩充（见 [roadmap.md](./roadmap.md)） |
| 阶段 3+ | ⏳ | React + FastAPI 等（有用户需求后再评估） |

## 核心功能模块

### 模块A：案例库（数据库）

- 分类收录真实历史/当代案例：
  - **共产党宣传**：中共口号、文革标语、官方媒体标题、领袖讲话片段。
  - **基督教传教**：福音布道词、耶稣语录、现代布道、教会宣传。
  - **伊斯兰教传教**：古兰经经文、哈迪斯、现代达瓦演讲。
- 每条案例标注：**来源、时代、技巧标签、心理机制、平行映射、公开出处**。
- 当前 **120 条**（CCP / 基督教 / 伊斯兰教 各 40 条）。
- 数据准则：仅收录**公开来源可核实**的原文；详见 [ETHICS.md](./ETHICS.md)。

### 模块B：多维度对比引擎

用户可选择 2–3 条案例进行对比，系统生成 **8 维雷达图**、平行映射，并支持 Markdown / JSON 报告导出。

### 模块C：可视化与分析工具

| 功能 | Streamlit | HTML 原型 (`index.html`) |
|------|-----------|--------------------------|
| 8 维话术矩阵 | ✅ 主页 + 可视化页 | ✅ 含矩阵点击筛选 |
| 词云 / 时间轴 / 雷达图 | ✅ | ✅ |
| 互动分析器 | ✅ 规则 + 相似度 | ✅ Jaccard 规则版 |
| 暗黑模式 | Streamlit 主题 | ✅ |

### 模块D：教育与互动

- 技巧拆解标签、8 维矩阵说明
- [伦理准则](./ETHICS.md) / [免责声明](./DISCLAIMER.md)（应用内页面 + Markdown）
- [GitHub Issues](https://github.com/HeisenbergSONG/Prophet-vs-Party/issues) 报告偏差
- 案例贡献表单（生成 JSON，通过 PR 提交）

## Streamlit 应用结构

```
app.py                 # 入口：主页 + st.navigation
pages/
  1_案例库.py          # 搜索、筛选、2–3 条对比、雷达图
  2_互动分析器.py      # 文本分析、相似案例、报告导出
  3_可视化.py          # 时间轴、词云、矩阵、分类统计
  4_反馈与贡献.py      # Issues 链接、贡献表单
  5_伦理准则.py
  6_免责声明.py
core/                  # 数据加载、分析器、可视化、报告
cases.json / matrix.json / rules.yaml
```

侧边栏提供：作者、GitHub 仓库、在线应用、伦理/免责文档、报告问题入口。  
移动端竖屏会提示**建议横屏使用**，以获得更好的图表与矩阵浏览体验。

## 本地运行

### Streamlit MVP（推荐，与线上一致）

```bash
cd "Prophet vs Party"
pip install -r requirements.txt          # 轻量版（与 Streamlit Cloud 一致）
# 或 pip install -r requirements-full.txt  # 完整版（含语义 embedding）
streamlit run app.py
```

浏览器打开 `http://localhost:8501`。

### HTML 静态原型（辅助演示）

```bash
python -m http.server 8080
```

浏览器打开 `http://localhost:8080/index.html`。  
需通过 HTTP 服务访问，以便加载 `cases.json` 与 `matrix.json`。

## 部署（Streamlit Community Cloud）

项目已**公开**部署至 Streamlit Cloud，可直接访问：https://prophet-vs-party.streamlit.app

| 项 | 值 |
|----|-----|
| 在线地址 | https://prophet-vs-party.streamlit.app（Public） |
| 仓库 | `HeisenbergSONG/Prophet-vs-Party` |
| 入口文件 | `app.py` |
| Python | 3.11 |
| 依赖 | `requirements.txt`（默认轻量版） |
| 系统包 | `packages.txt`（中文字体，词云用） |

重新部署步骤（新 fork 或重装时）：

1. 登录 [share.streamlit.io](https://share.streamlit.io)
2. **New app** → 选择仓库 → Main file path：`app.py`
3. Advanced：Python **3.11**，Dependencies file：`requirements.txt`
4. Deploy → 在控制台确认状态为 **Running**

| 依赖文件 | 适用场景 |
|----------|----------|
| `requirements.txt` | **默认 / Cloud 部署**：轻量版，相似度用 Jaccard + 规则 |
| `requirements-full.txt` | **本地完整版**：含 `torch` + `sentence-transformers` 语义相似度 |

**隐私**：用户输入仅在会话内分析，不写入数据库；详见 [ETHICS.md](./ETHICS.md)。

## 数据格式

案例 JSON 字段说明（见 `sample_standard.json`）：

| 字段 | 说明 |
|------|------|
| `id` | 唯一标识 |
| `source_type` | `ccp` / `christian` / `islam` |
| `text` | 原文 |
| `source` | 出处名称 |
| `source_url` | 可核实的公开来源（人类可读描述） |
| `source_link` | 可点击 URL（可选，`source_type_ref=link` 时必填） |
| `source_type_ref` | `link` / `citation` / `archive` |
| `source_verified` | 是否已核对引文 |
| `techniques` | 修辞技巧标签 |
| `parallel` | 跨类型平行映射 |
| `year_start` / `year_end` / `era` | 时代标注 |

## 技术架构

| 层级 | 当前技术栈 |
|------|------------|
| 主应用 | Streamlit 1.36+、`st.navigation`、Plotly、WordCloud |
| 分析 | `rules.yaml` 规则引擎 + Jaccard（Cloud）/ sentence-transformers（本地可选） |
| 静态原型 | HTML + Tailwind + Chart.js + WordCloud2 |
| 测试 | pytest（16 项）+ GitHub Actions |
| 中期规划 | React + TypeScript + FastAPI（见 roadmap） |

## 文档

- [路线图](./roadmap.md) — 阶段进度与 KPI
- [伦理与数据准则](./ETHICS.md)
- [免责声明](./DISCLAIMER.md)

## 测试与 CI

```bash
pip install -r requirements-ci.txt
pytest tests/ -v
```

推送至 `main` 后，GitHub Actions 自动运行测试（`.github/workflows/ci.yml`）。

## 贡献

详见 **[CONTRIBUTING.md](./CONTRIBUTING.md)**（案例格式、PR 自检、伦理边界）。

- 引文/来源错误 → [报告偏差 Issue](https://github.com/HeisenbergSONG/Prophet-vs-Party/issues/new?template=source-error.yml)
- 新案例 → 应用内「反馈与贡献」生成 JSON → Pull Request 更新 `cases.json`
- 功能建议 / Bug → [Issue 模板](https://github.com/HeisenbergSONG/Prophet-vs-Party/issues/new/choose)

## 开源协议

本项目采用 [GNU General Public License v3.0 (GPLv3)](./LICENSE) 开源。

---

**说明**：本设计为教育/学术用途，保持中立分析。