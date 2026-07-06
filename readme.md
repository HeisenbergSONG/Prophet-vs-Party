# 程序设计方案：宣传 vs 传教对比分析平台

**名称**：  
**Prophet vs Party**（先知 vs 政党）  
或中文名：**「话语之战」——共产党宣传与宗教传教对比分析平台**

## 定位

一个**中立、教育性**的交互式工具，帮助用户系统地对比**共产党（以中共为代表）宣传话术**与**基督教、伊斯兰教传教话术**的异同。  
核心目标是**分析修辞技巧、心理机制、动员策略**，而非评判优劣。

## 核心功能模块

### 模块A：案例库（数据库）

- 分类收录真实历史/当代案例：
  - **共产党宣传**：中共口号、文革标语、官方媒体标题、领袖讲话片段。
  - **基督教传教**：福音布道词、耶稣语录、现代布道、教会宣传。
  - **伊斯兰教传教**：古兰经经文、哈迪斯、现代达瓦演讲。
- 每条案例标注：**来源、时代、技巧标签、心理机制、平行映射、公开出处**。
- 数据准则：仅收录**公开来源可核实**的原文；详见 [ETHICS.md](./ETHICS.md)。

### 模块B：多维度对比引擎

用户可选择 2–3 条案例进行对比，系统生成分析报告（雷达图、平行映射、Markdown/JSON 导出）。

### 模块C：可视化与分析工具

- 话术矩阵（8 维度可点击筛选）
- 词云、时间轴、雷达图
- 互动分析器（规则匹配 + 相似案例推荐）

### 模块D：教育与互动

- 技巧拆解标签
- 免责声明与偏差报告入口

## 本地运行

### Streamlit MVP（推荐）

```bash
cd "Prophet vs Party"
pip install -r requirements.txt
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501`。

### HTML 静态原型

```bash
python -m http.server 8080
```

浏览器打开 `http://localhost:8080/index.html`。

> HTML 需通过 HTTP 服务访问，以便加载 `cases.json` 与 `matrix.json`。

## 部署到 Streamlit Community Cloud（方案 A）

1. 将代码推送到 GitHub 仓库 `HeisenbergSONG/Prophet-vs-Party`
2. 登录 [share.streamlit.io](https://share.streamlit.io)，用 GitHub 授权
3. **New app** → 选择仓库 → Main file path 填 `app.py`
4. **Advanced settings**：
   - Python version：**3.11**
   - Dependencies file：**`requirements-cloud.txt`**（推荐，无 torch，启动快）
5. 点击 **Deploy**

| 依赖文件 | 适用场景 |
|----------|----------|
| `requirements-cloud.txt` | **Cloud 推荐**：轻量、省内存，相似度用 Jaccard |
| `requirements.txt` | 本地完整版：含 `torch` + `sentence-transformers` 语义相似度 |

**在线地址**（部署后填写）：`https://<your-app>.streamlit.app`

**隐私**：用户输入仅在会话内分析，不写入数据库；详见 `ETHICS.md`。

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

| 阶段 | 技术栈 |
|------|--------|
| 当前原型 | HTML + Tailwind + Chart.js + WordCloud2 |
| MVP | Streamlit (Python) |
| 中期 | React + TypeScript + FastAPI |

## 文档

- [路线图](./roadmap.md)
- [伦理与数据准则](./ETHICS.md) — 公开来源可核实即视为事实，无需人工审核
- [免责声明](./DISCLAIMER.md)

## 测试与 CI

```bash
pip install -r requirements-ci.txt
pytest tests/ -v
```

推送至 `main` 后，GitHub Actions 自动运行测试（见 `.github/workflows/ci.yml`）。

## 贡献

发现引文或来源错误，请提交 [GitHub Issues](https://github.com/HeisenbergSONG/Prophet-vs-Party/issues)，附可核实的正确出处。

## 开源协议

本项目采用 [GNU General Public License v3.0 (GPLv3)](./LICENSE) 开源。

---

**说明**：本设计为教育/学术用途，保持中立分析。