import httpx
import json
import os
import re
from typing import List, Dict

# Configuration
SITE_URL = "https://carnivore.kematconsulting.co.uk"
# WooCommerce Store API (Public)
WP_API_URL = f"{SITE_URL}/wp-json/wc/store/products?per_page=100"
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
OUTPUT_FILE = os.path.join(DATA_DIR, "menu.json")

def clean_html(raw_html: str) -> str:
    if not raw_html: return ""
    # Remove HTML tags
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # Remove newlines and extra spaces
    cleantext = cleantext.replace('\n', ' ').strip()
    return cleantext

def generate_id(name: str) -> str:
    return name.lower().replace(" ", "_").replace("'", "").replace("-", "_").replace("(", "").replace(")", "")

async def sync_menu():
    print(f"Fetching menu from {WP_API_URL}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        try:
            response = await client.get(WP_API_URL)
            response.raise_for_status()
            products = response.json()
        except Exception as e:
            print(f"Error fetching from WordPress: {e}")
            return False

    menu_items = []
    for p in products:
        name = p.get('name', 'Unknown')
        
        # Price mapping (handle minor units)
        price_data = p.get('prices', {})
        raw_price = price_data.get('price', '0')
        minor_units = price_data.get('currency_minor_unit', 2)
        try:
            price_val = float(raw_price) / (10 ** minor_units)
            price_str = f"{price_val:.2f}"
        except:
            price_str = "0.00"

        # Description (Short description usually contains ingredients)
        desc = clean_html(p.get('short_description', ''))
        
        # Category
        cats = p.get('categories', [])
        category = cats[0].get('name', 'General') if cats else 'General'
        
        item = {
            "id": generate_id(name),
            "wp_id": str(p.get('id', '')),
            "name": name,
            "price": price_str,
            "description": desc,
            "category": category,
            "tags": [category.lower()]
        }
        menu_items.append(item)
        print(f"Synced: {name} (£{price_str})")

    # Enforce Baked Meat price just in case of website mismatch (as per Phase 11)
    for item in menu_items:
        if "baked meat" in item['name'].lower():
            item['price'] = "94.99"

    # Save to file
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(menu_items, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully synced {len(menu_items)} items to {OUTPUT_FILE}")
    return True

if __name__ == "__main__":
    import asyncio
    asyncio.run(sync_menu())
