#!/usr/bin/env python3
"""Sync prices.json from the public llmabacus pricing API.

历史包袱与改法（2026-08-02）：本脚本原先读一个写死的本机绝对路径
（/Users/szp2005/ClaudeCode/llmabacus/src/data/models.json）。那个源仓是私有的，
所以这份公开数据集**结构上不可能挂 CI 自动同步**——于是它对外挂着「每日核价」
却实际停在 2026-07-03 整整 30 天。

改为从公开 API https://www.llmabacus.com/api/prices 取数：
  - 零密钥、零跨仓 token（源是公开端点，不需要访问私有仓）
  - 因此可以挂 GitHub Action 日更（见 .github/workflows/daily-sync.yml）
  - 取到的就是站点对外承诺的同一份数据，不存在「站内一份、数据集另一份」的漂移

字段口径（两个都别再漏）：
  - last_checked ≠ last_updated：前者是「最近一次对官方页核对的日期」，
    后者是「最近一次价格实际变动的日期」。价格没变时 last_updated 不动，
    只导出 last_updated 会让消费方误判数据陈旧（本项目 2026-07-24 就这么误判过一次）。
  - price_tiers：长上下文阶梯价。基础价是**首档**价，用满长上下文必然跨档，
    只按首档算最高低估 6 倍（qwen3-5-flash ¥0.20→¥1.20）。
    API 已同时给出 CNY 换算价与原币价，此处原样透传，**不再自行乘汇率**
    （CNY 计价厂商乘汇率会得到假价格）。
"""
import json
import os
import sys
import urllib.request

API_URL = os.environ.get("LLMABACUS_API_URL", "https://www.llmabacus.com/api/prices")
TIMEOUT = int(os.environ.get("SYNC_TIMEOUT", "30"))


def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "llm-prices-cn-sync/2.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        # urlopen 对 4xx/5xx 已抛 HTTPError，这里是兜底。
        # status 为 None 的情况是非 HTTP scheme（本地 file:// 回归测试用），不判死。
        status = getattr(resp, "status", None)
        if status is not None and status != 200:
            raise RuntimeError(f"API returned HTTP {status}")
        return json.loads(resp.read().decode("utf-8"))


def transform(src: dict) -> dict:
    meta = src.get("meta", {})
    vendors = {v["id"]: v for v in src.get("vendors", [])}

    models = []
    for m in src.get("models", []):
        vendor = vendors.get(m.get("vendorId"), {})
        currency = m.get("priceCurrency") or vendor.get("currency", "CNY")

        out = {
            "id": m.get("id"),
            "name": m.get("name"),
            "vendor_id": m.get("vendorId"),
            "vendor_name": vendor.get("name", m.get("vendorId")),
            "country": vendor.get("country", ""),
            "billing_currency": currency,
            # CNY 为 API 已换算值；原币价直接来自厂商官方页，二者都不在此处再算
            "input_price_cny_per_m": m.get("inputPrice"),
            "output_price_cny_per_m": m.get("outputPrice"),
            "cached_input_price_cny_per_m": m.get("cachedInputPrice"),
            "input_price_orig_per_m": m.get("inputPriceOrig"),
            "output_price_orig_per_m": m.get("outputPriceOrig"),
            "cached_input_price_orig_per_m": m.get("cachedInputPriceOrig"),
            "context_window": m.get("contextWindow"),
            "max_output": m.get("maxOutput"),
            "modality": m.get("modality", ["text"]),
            "tags": m.get("tags", []),
            "retired": m.get("retired", False),
            "knowledge_cutoff": m.get("knowledgeCutoff"),
            "quality_score": m.get("quality"),
            "source": m.get("source"),
            "last_verified": m.get("lastVerified"),
        }

        # 阶梯价：有才带，且原样透传（upTo=null 表示最高档无上限）
        if m.get("tiers"):
            out["price_tiers"] = [
                {
                    "up_to_input_tokens": t.get("upTo"),
                    "input_price_cny_per_m": t.get("inputPrice"),
                    "output_price_cny_per_m": t.get("outputPrice"),
                    "cached_input_price_cny_per_m": t.get("cachedInputPrice"),
                    "input_price_orig_per_m": t.get("inputPriceOrig"),
                    "output_price_orig_per_m": t.get("outputPriceOrig"),
                    "cached_input_price_orig_per_m": t.get("cachedInputPriceOrig"),
                }
                for t in m["tiers"]
            ]
            out["price_tiers_source"] = m.get("tiersSource")
            out["price_tiers_note"] = (
                "Billed by the tier matching a single request's input token count; "
                "the whole request is charged at that tier. Base price above = first tier."
            )

        models.append(out)

    return {
        # 最近一次对官方定价页核对的日期（价格没变也会更新）
        "last_checked": meta.get("lastChecked"),
        # 最近一次价格实际发生变动的日期
        "last_updated": meta.get("lastUpdated"),
        "usd_to_cny_rate": meta.get("usdToCny"),
        "usd_to_cny_updated": meta.get("usdToCnyUpdated"),
        "pricing_unit": meta.get("unit", "per_million_tokens"),
        "model_count": len(models),
        "license": "CC-BY-4.0",
        "source": "https://www.llmabacus.com",
        "api": API_URL,
        "models": models,
    }


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, "prices.json")

    print(f"Fetching {API_URL} ...")
    try:
        src = fetch(API_URL)
    except Exception as exc:  # noqa: BLE001 - CI 需要看到真实原因
        print(f"ERROR: fetch failed: {exc}", file=sys.stderr)
        return 1

    data = transform(src)

    # 健全性闸：宁可不更新，也不要把空数据/坏数据推成「今日已核对」
    if data["model_count"] < 20:
        print(f"ERROR: only {data['model_count']} models, refusing to write", file=sys.stderr)
        return 1
    if not data["last_checked"]:
        print("ERROR: meta.lastChecked missing, refusing to write", file=sys.stderr)
        return 1
    missing = [m["id"] for m in data["models"] if m.get("input_price_cny_per_m") is None]
    if missing:
        print(f"ERROR: {len(missing)} models missing price: {missing[:5]}", file=sys.stderr)
        return 1

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    tiered = sum(1 for m in data["models"] if "price_tiers" in m)
    print(
        f"Wrote {data['model_count']} models ({tiered} with price tiers) to {out_path}\n"
        f"  last_checked={data['last_checked']}  last_updated={data['last_updated']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
