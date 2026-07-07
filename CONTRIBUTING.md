# Contributing to LLM API Pricing Dataset (贡献指南)

[English](#english) | [中文](#中文)

---

## English

Thank you for your interest in helping us maintain the most accurate and up-to-date LLM API pricing dataset!

### How You Can Help
1. **Report Price Changes**: If you notice that a model's official pricing has changed but our dataset hasn't updated yet, please open an Issue.
2. **Report Errors**: Spot a typo or wrong value in `prices.json`? Let us know!
3. **Request New Models**: Want us to track a new model? Suggest it by opening an Issue.

### Contribution Rules
- **Verify with Official Sources**: Any price change report or correction **must** be accompanied by a link to the official vendor documentation or billing page. We do not accept pricing claims based on blog posts, news articles, or third-party aggregators.
- **Do Not Modify `prices.json` Directly**: `prices.json` is automatically generated from the source code configuration of [LLM Abacus](https://llmabacus.com). If you wish to submit a price correction, please open an issue or submit a pull request modifying the upstream model configurations (if you are a developer) rather than editing `prices.json` directly.

---

## 中文

感谢您关注并帮助我们共同维护最准确、最及时的大模型 API 价格数据集！

### 如何参与贡献
1. **反馈价格变动**：如果您发现某个大模型的官方定价已经调整，但本仓库的快照尚未更新，请提交 Issue。
2. **纠正数据错误**：如果您发现 `prices.json` 中的某个模型参数（如上下文窗口、最大输出）有误，欢迎向我们反馈。
3. **申请新增模型**：如果您希望我们收录并跟踪新的大模型 API，请开 Issue 提交申请。

### 贡献规则与要求
- **以官方信源为准**：任何关于价格变更或纠错的反馈，**必须**附带该模型官方网站的计费文档或文档页链接。我们不接受第三方博客、媒体报道或中介聚合站的价格口径。
- **不要直接修改 `prices.json`**：`prices.json` 是通过 [LLM Abacus](https://llmabacus.com) 主站的自动化脚本与配置文件生成的。如需进行价格修正，请提交 Issue 反馈，或通过开发者 PR 调整主站上游配置文件，请勿直接编辑 `prices.json`。
