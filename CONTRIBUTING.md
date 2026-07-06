# 贡献指南

感谢参与 **Prophet vs Party（话语之战）**。本项目为零成本开源教育项目，欢迎通过 GitHub 提交 Issue 与 Pull Request。

## 开始前请阅读

- [ETHICS.md](./ETHICS.md) — 仅收录**公开来源可核实**的原文
- [DISCLAIMER.md](./DISCLAIMER.md) — 中立教育定位
- [sample_standard.json](./sample_standard.json) — 单条案例字段示例

## 你可以如何贡献

| 类型 | 方式 |
|------|------|
| 引文/来源错误 | [报告偏差 Issue](https://github.com/HeisenbergSONG/Prophet-vs-Party/issues/new?template=source-error.yml) |
| 新增案例 | PR 修改 `cases.json`（见下文） |
| 规则与技巧标签 | PR 修改 `rules.yaml` |
| 矩阵维度说明 | PR 修改 `matrix.json` |
| 功能建议 / Bug | [Issue 模板](https://github.com/HeisenbergSONG/Prophet-vs-Party/issues/new/choose) |

也可在应用内 **反馈与贡献** 页面生成 JSON 草稿，再发起 PR。

## 新增案例（cases.json）

### 1. 平衡原则

- 三类 `ccp` / `christian` / `islam` 尽量同步增加，保持约 **1:1:1**
- `id` 格式：`{source_type}_{三位序号}`，如 `ccp_021`（勿与现有 id 重复）

### 2. 必填字段

| 字段 | 说明 |
|------|------|
| `text` | 可核实的原文（勿改写） |
| `source` | 出处名称（经典、演讲、媒体等） |
| `source_url` | 人类可读的来源描述 |
| `source_type_ref` | `link` / `citation` / `archive` |
| `source_link` | `link` 类型时必填可点击 URL |
| `source_verified` | 贡献者是否已核对（bool） |
| `techniques` | 修辞技巧标签数组 |
| `year_start` / `year_end` / `era` | 时代标注 |

### 3. 建议一并填写

- `category`、`psychological_mechanism`
- `parallel`：另两类的平行映射（中立对照，非价值判断）
- `risk_note`：必要时注明误读风险

### 4. PR 自检清单

- [ ] 原文可在公开来源核对
- [ ] `id` 唯一，三类比例未严重失衡
- [ ] `source_type_ref=link` 时 `source_link` 有效
- [ ] 本地运行 `pytest tests/ -v` 通过
- [ ] 未加入无法核实或明显断章取义的片段

## 本地验证

```bash
pip install -r requirements-ci.txt
pytest tests/ -v
```

## 行为准则

- 保持**中立修辞分析**立场，不做传教或宣传
- 争议内容以可核实出处为准，避免口水战式 Issue
- 尊重 GPLv3：衍生作品需开源并标注修改

## 联系

- 仓库：https://github.com/HeisenbergSONG/Prophet-vs-Party
- 在线应用：https://prophet-vs-party.streamlit.app