#!/usr/bin/env python3
import os
import json
from datetime import datetime

def sync_prices():
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Target paths
    llmabacus_models_path = "/Users/szp2005/ClaudeCode/llmabacus/src/data/models.json"
    output_prices_path = os.path.join(script_dir, "prices.json")
    
    if not os.path.exists(llmabacus_models_path):
        print(f"Error: Source models.json not found at {llmabacus_models_path}")
        return False
        
    print(f"Reading source models from: {llmabacus_models_path}")
    with open(llmabacus_models_path, "r", encoding="utf-8") as f:
        src_data = json.load(f)
        
    usd_to_cny = src_data.get("usdToCny", 6.7855)
    last_updated = src_data.get("lastUpdated", datetime.now().strftime("%Y-%m-%d"))
    usd_to_cny_updated = src_data.get("usdToCnyUpdated", "")
    
    vendors = src_data.get("vendors", {})
    src_models = src_data.get("models", [])
    
    formatted_models = []
    for model in src_models:
        vendor_id = model.get("vendorId")
        vendor_info = vendors.get(vendor_id, {})
        vendor_name = vendor_info.get("name", vendor_id)
        vendor_country = vendor_info.get("country", "")
        vendor_currency = vendor_info.get("currency", "CNY") # Default to CNY if not specified
        
        # Original price values from models.json
        input_price = model.get("inputPrice", 0.0)
        output_price = model.get("outputPrice", 0.0)
        cached_input_price = model.get("cachedInputPrice")
        
        # Calculate pricing in USD and CNY
        # Rule: USD billing vendors store values in USD, CNY billing vendors store values in CNY.
        if vendor_currency == "USD":
            input_usd = input_price
            output_usd = output_price
            cached_input_usd = cached_input_price
            
            input_cny = round(input_price * usd_to_cny, 4)
            output_cny = round(output_price * usd_to_cny, 4)
            cached_input_cny = round(cached_input_price * usd_to_cny, 4) if cached_input_price is not None else None
        else: # CNY billing
            input_cny = input_price
            output_cny = output_price
            cached_input_cny = cached_input_price
            
            input_usd = round(input_price / usd_to_cny, 4)
            output_usd = round(output_price / usd_to_cny, 4)
            cached_input_usd = round(cached_input_price / usd_to_cny, 4) if cached_input_price is not None else None
            
        formatted_model = {
            "id": model.get("id"),
            "name": model.get("name"),
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
            "country": vendor_country,
            "billing_currency": vendor_currency,
            "input_price_usd_per_m": input_usd,
            "output_price_usd_per_m": output_usd,
            "input_price_cny_per_m": input_cny,
            "output_price_cny_per_m": output_cny,
        }
        
        if cached_input_usd is not None:
            formatted_model["cached_input_price_usd_per_m"] = cached_input_usd
            formatted_model["cached_input_price_cny_per_m"] = cached_input_cny
            
        formatted_model.update({
            "context_window": model.get("contextWindow"),
            "max_output": model.get("maxOutput"),
            "modality": model.get("modality", ["text"]),
            "tags": model.get("tags", []),
            "knowledge_cutoff": model.get("knowledgeCutoff", "")
        })
        
        if "quality" in model:
            formatted_model["quality_score"] = model["quality"]
            
        formatted_models.append(formatted_model)
        
    dest_data = {
        "last_updated": last_updated,
        "usd_to_cny_rate": usd_to_cny,
        "usd_to_cny_updated": usd_to_cny_updated,
        "pricing_unit": "per_million_tokens",
        "license": "CC-BY-4.0",
        "source": "https://llmabacus.com",
        "models": formatted_models
    }
    
    # Create directory if it doesn't exist
    os.makedirs(script_dir, exist_ok=True)
    
    with open(output_prices_path, "w", encoding="utf-8") as f:
        json.dump(dest_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully synced {len(formatted_models)} models to: {output_prices_path}")
    return True

if __name__ == "__main__":
    sync_prices()
