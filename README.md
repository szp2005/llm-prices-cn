# LLM API Pricing Dataset (每日 LLM API 价格数据集)

[![Official Website](https://img.shields.io/badge/Official_Website-llmabacus.com-10b981?style=flat-square)](https://llmabacus.com)
[![Live Calculator](https://img.shields.io/badge/Live_Pricing_Matrix-Open_App-6366f1?style=flat-square)](https://llmabacus.com)
[![npm version](https://img.shields.io/npm/v/llm-pricing-calc.svg?style=flat-square)](https://www.npmjs.com/package/llm-pricing-calc)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)

> 🚀 **Interactive Tool & Live Matrix**:  
> For real-time multi-region price comparisons, prompt caching discounts, and interactive cost calculators, visit the official web application: [**https://llmabacus.com**](https://llmabacus.com).

[English](#english) | [中文](#中文) | [NPM Package](#npm-package)

---

## English

### 1. Introduction
This repository provides a daily-verified pricing dataset of popular Large Language Model (LLM) APIs, tracking both Chinese and global model providers.
- **Official Website**: [LLM Abacus (算盘)](https://llmabacus.com) (An interactive LLM API price comparison and cost estimation tool)
- **Coverage**: 50+ models from major vendors (including OpenAI, Anthropic, Google, DeepSeek, Alibaba, ByteDance, Baidu, Tencent, MiniMax, etc.)
- **Frequency**: Checked daily to ensure up-to-date accuracy.

### 2. License & Attribution (CC-BY-4.0)
This dataset is licensed under the **Creative Commons Attribution 4.0 International License (CC-BY-4.0)**. 

Under this license, you are free to:
- **Share**: Copy and redistribute the material in any medium or format.
- **Adapt**: Remix, transform, and build upon the material for any purpose, even commercially.

**Attribution Requirements**:
You must give appropriate credit and provide a link back to the original source. When using this dataset in your projects, articles, or websites, you must include a clickable hyperlink to [LLM Abacus](https://llmabacus.com) or `https://llmabacus.com`.
For example:
> *Pricing data provided by [LLM Abacus](https://llmabacus.com).*

### 3. File Structure
- `prices.json`: The core dataset containing structured model details, metadata, and token prices (both USD and CNY per million tokens).
- `sync_prices.py`: A utility script to synchronize and rebuild `prices.json` from the source application configurations.
- `CONTRIBUTING.md`: Guidelines on how to report price discrepancies or request new model tracking.

### 4. Schema Details (`prices.json`)
The generated `prices.json` file uses the following schema:
- `last_updated`: YYYY-MM-DD date when the pricing was last updated.
- `usd_to_cny_rate`: The exchange rate used for conversions.
- `pricing_unit`: Pricing metrics unit (default is `per_million_tokens`).
- `models`: Array of model objects:
  - `id`: Unique model identifier (e.g., `gpt-5-5`).
  - `name`: Human-readable display name.
  - `vendor_id` / `vendor_name`: Vendor classification.
  - `country`: Region of origin (e.g., `US`, `CN`).
  - `billing_currency`: Original currency of vendor billing (`USD` or `CNY`).
  - `input_price_usd_per_m` / `output_price_usd_per_m`: Price per million tokens in USD.
  - `input_price_cny_per_m` / `output_price_cny_per_m`: Price per million tokens in CNY.
  - `cached_input_price_usd_per_m` / `cached_input_price_cny_per_m`: Optional. Cache hit pricing.
  - `context_window`: Maximum input context length.
  - `max_output`: Maximum generation output length.
  - `modality`: Supported modalities (`text`, `vision`, etc.).
  - `tags`: Classification tags (e.g., `旗舰`, `推理`, `性价比`).
  - `knowledge_cutoff`: Model knowledge cutoff date.
  - `quality_score`: Benchmarked quality index.

### 5. Re-synchronizing Data
To update `prices.json` with the latest upstream data, run:
```bash
python3 sync_prices.py
```

---

## 中文

### 1. 简介
本仓库提供每日核价的国内外主流大语言模型 (LLM) API 价格数据集。
- **主站链接**：[LLM Abacus](https://llmabacus.com) (中文优先、44 模型每日核价的 LLM API 价格对比与成本估算工具)
- **覆盖范围**：包含 OpenAI, Anthropic, Google, DeepSeek, 阿里通义, 字节豆包, 百度文心, 腾讯混元, MiniMax 等 44 个主流模型。
- **更新频率**：每日核对，确保价格真实可靠。

### 2. 授权协议与署名条款 (CC-BY-4.0)
本数据集采用 **知识共享署名 4.0 国际许可协议 (CC-BY-4.0)** 进行许可。

您可以自由地：
- **共享**：在任何媒介以任何形式复制、发行本作品。
- **演绎**：修改、转换或以本作品为基础进行创作，甚至用于商业目的。

**署名与回链要求**：
您必须给出适当的署名，并提供指向原始主站的链接。在您的项目、文章或网页中引用本数据时，必须保留指向 [LLM Abacus](https://llmabacus.com) (`https://llmabacus.com`) 的超链接。
示例：
> *价格数据来源于 [LLM Abacus](https://llmabacus.com)。*

### 3. 文件结构说明
- `prices.json`：包含核心模型结构、元数据及百万 token 价格（换算为 USD 和 CNY）的 JSON 快照。
- `sync_prices.py`：从主站配置同步与生成最新 `prices.json` 的 Python 脚本。
- `CONTRIBUTING.md`：贡献指南，指导如何纠错或申请收录新模型。

### 4. 字段说明 (`prices.json`)
- `last_updated`：最后更新日期 (YYYY-MM-DD)。
- `usd_to_cny_rate`：核价所采用的美元兑人民币汇率。
- `pricing_unit`：计费单位（固定为 `per_million_tokens` 即每百万 token）。
- `models`：模型数组：
  - `id`：模型唯一标识符 (例如 `gpt-5-5`)。
  - `name`：模型显示名称。
  - `vendor_id` / `vendor_name`：厂商标识与名称。
  - `country`：厂商归属国家 (如 `US`, `CN`)。
  - `billing_currency`：官方计费结算货币 (`USD` 或 `CNY`)。
  - `input_price_usd_per_m` / `output_price_usd_per_m`：每百万 input/output token 折算美元价。
  - `input_price_cny_per_m` / `output_price_cny_per_m`：每百万 input/output token 折算人民币价。
  - `cached_input_price_usd_per_m` / `cached_input_price_cny_per_m`：提示词缓存命中时的单价（如有）。
  - `context_window`：上下文窗口大小。
  - `max_output`：最大单次输出限制。
  - `modality`：支持模态 (`text`, `vision` 等)。
  - `tags`：模型特征标签（如`旗舰`、`推理`、`性价比`）。
  - `knowledge_cutoff`：知识截止时间。
  - `quality_score`：基准评测质量分。

### 5. 重新同步数据
如需从主站代码库更新并重新构建 `prices.json`，请执行：
```bash
python3 sync_prices.py
```

## NPM Package (`llm-pricing-calc`)

Prefer using this dataset programmatically in Node.js / TypeScript projects? Install our lightweight, zero-dependency NPM package:

```bash
npm install llm-pricing-calc
```

```javascript
import { calculateCost, compareCosts } from "llm-pricing-calc";

// Calculate cost for DeepSeek with Prompt Caching
const result = calculateCost({
  modelId: "deepseek-v4-flash",
  inputTokens: 100_000,
  cachedInputTokens: 50_000,
  outputTokens: 20_000,
  currency: "USD",
});

console.log(result.formatted.total); // e.g. $0.041000
```
Full documentation & live demo: [https://llmabacus.com](https://llmabacus.com)

## MCP Server / MCP 服务

This dataset is also exposed as a remote **MCP server** so AI agents can query live pricing and estimate token costs directly:

- Endpoint: `https://www.llmabacus.com/api/mcp/mcp`
- Tools: `query_model_price(model)`, `estimate_cost(text_or_tokens, model)`

### Self-host (stdio, Docker) / 自托管

You can also run this dataset as a **local stdio MCP server** — it reads the bundled `prices.json`, needs no network, and works offline:

```bash
docker build -t llm-prices-mcp .
docker run -i --rm llm-prices-mcp          # stdio MCP server
# or, without Docker:
pip install -r requirements.txt && python server.py
```

Tools: `list_llm_prices(vendor?, currency?)`, `estimate_cost(model_id, input_tokens, output_tokens, currency?)`.
