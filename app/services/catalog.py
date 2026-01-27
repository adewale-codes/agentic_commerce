import json
from pathlib import Path
from typing import List, Optional
from app.core.config import settings
from app.agent.schemas import Product, Constraints

_products_cache: List[Product] | None = None

def load_products() -> List[Product]:
    global _products_cache
    if _products_cache is not None:
        return _products_cache

    path = Path(settings.data_path)
    if not path.exists():
        raise FileNotFoundError(f"Products file not found at: {path.resolve()}")

    raw = json.loads(path.read_text(encoding="utf-8"))
    _products_cache = [Product(**p) for p in raw]
    return _products_cache

def _matches_query(p: Product, query: Optional[str]) -> bool:
    if not query:
        return True
    q = query.lower().strip()
    hay = f"{p.title} {p.brand} {p.attributes.get('cpu','')} {p.attributes.get('os','')}".lower()
    return q in hay

def search_products(query: Optional[str], c: Constraints, limit: int | None = None) -> List[Product]:
    products = load_products()
    limit = limit or settings.max_search_results

    out: List[Product] = []
    for p in products:
        if p.category != "laptop":
            continue
        if c.in_stock_only and not p.in_stock:
            continue
        if c.max_price_gbp is not None and p.price_gbp > c.max_price_gbp:
            continue
        if c.shipping_days_max is not None and p.shipping_days > c.shipping_days_max:
            continue

        ram = int(p.attributes.get("ram_gb", 0))
        storage = int(p.attributes.get("storage_gb", 0))
        battery = float(p.attributes.get("battery_hours", 0))
        weight = float(p.attributes.get("weight_kg", 999))

        if c.min_ram_gb is not None and ram < c.min_ram_gb:
            continue
        if c.min_storage_gb is not None and storage < c.min_storage_gb:
            continue
        if c.min_battery_hours is not None and battery < c.min_battery_hours:
            continue
        if c.max_weight_kg is not None and weight > c.max_weight_kg:
            continue
        if c.os is not None and str(p.attributes.get("os", "")).lower() != c.os.lower():
            continue

        if not _matches_query(p, query):
            continue

        out.append(p)
        if len(out) >= limit:
            break

    return out
