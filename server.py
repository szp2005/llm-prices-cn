"""Self-hostable MCP server for the LLM Abacus daily-verified price dataset.

Exposes the committed `prices.json` snapshot (44 China + overseas models, CNY/USD
dual pricing) over the Model Context Protocol so AI agents can query live-ish
pricing and estimate token costs locally — no network required.

Data source & attribution: https://llmabacus.com (CC-BY-4.0).
Run: `python server.py` (stdio transport) — or via the bundled Dockerfile.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

_DATA = json.loads((Path(__file__).parent / "prices.json").read_text(encoding="utf-8"))
_MODELS = _DATA["models"]

mcp = FastMCP("llm-prices-cn")


def _price_keys(currency: str) -> tuple[str, str]:
    cur = (currency or "CNY").upper()
    if cur == "USD":
        return "input_price_usd_per_m", "output_price_usd_per_m"
    return "input_price_cny_per_m", "output_price_cny_per_m"


@mcp.tool()
def list_llm_prices(vendor: Optional[str] = None, currency: str = "CNY") -> dict:
    """List daily-verified LLM API prices (per 1M tokens).

    Args:
        vendor: optional filter, matched against vendor name/id (e.g. "deepseek", "openai").
        currency: "CNY" (default) or "USD".
    """
    ki, ko = _price_keys(currency)
    rows = _MODELS
    if vendor:
        v = vendor.lower()
        rows = [m for m in rows if v in f"{m['vendor_name']}{m['vendor_id']}".lower()]
    return {
        "last_updated": _DATA.get("last_updated"),
        "usd_to_cny_rate": _DATA.get("usd_to_cny_rate"),
        "currency": (currency or "CNY").upper(),
        "unit": "per 1M tokens",
        "source": "https://llmabacus.com",
        "count": len(rows),
        "models": [
            {
                "id": m["id"],
                "name": m["name"],
                "vendor": m["vendor_name"],
                "input": m[ki],
                "output": m[ko],
                "context_window": m.get("context_window"),
            }
            for m in rows
        ],
    }


@mcp.tool()
def estimate_cost(
    model_id: str,
    input_tokens: int,
    output_tokens: int,
    currency: str = "CNY",
) -> dict:
    """Estimate the cost of a single request for a given model and token counts.

    Args:
        model_id: model id from list_llm_prices (e.g. "deepseek-v4-pro").
        input_tokens: number of input (prompt) tokens.
        output_tokens: number of output (completion) tokens.
        currency: "CNY" (default) or "USD".
    """
    m = next((x for x in _MODELS if x["id"] == model_id), None)
    if m is None:
        return {
            "error": f"model '{model_id}' not found",
            "hint": "call list_llm_prices to see available model ids",
        }
    ki, ko = _price_keys(currency)
    cost = input_tokens / 1_000_000 * m[ki] + output_tokens / 1_000_000 * m[ko]
    return {
        "model": m["name"],
        "model_id": m["id"],
        "currency": (currency or "CNY").upper(),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost": round(cost, 6),
        "source": "https://llmabacus.com",
    }


if __name__ == "__main__":
    mcp.run()  # stdio transport by default
