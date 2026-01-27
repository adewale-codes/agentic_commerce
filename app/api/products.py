from fastapi import APIRouter, Query
from typing import Optional
from app.agent.schemas import Constraints, Product
from app.services.catalog import search_products

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/search", response_model=list[Product])
def products_search(
    q: Optional[str] = Query(default=None),
    max_price_gbp: Optional[float] = None,
    min_ram_gb: Optional[int] = None,
    min_storage_gb: Optional[int] = None,
    min_battery_hours: Optional[float] = None,
    max_weight_kg: Optional[float] = None,
    os: Optional[str] = None,
    shipping_days_max: Optional[int] = None,
    in_stock_only: bool = True,
):
    c = Constraints(
        max_price_gbp=max_price_gbp,
        min_ram_gb=min_ram_gb,
        min_storage_gb=min_storage_gb,
        min_battery_hours=min_battery_hours,
        max_weight_kg=max_weight_kg,
        os=os,
        shipping_days_max=shipping_days_max,
        in_stock_only=in_stock_only,
    )
    return search_products(query=q, c=c)
