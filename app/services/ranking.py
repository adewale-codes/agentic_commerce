from typing import List, Tuple
from app.agent.schemas import Product, Constraints, RankedProduct

def rank_products(products: List[Product], c: Constraints, top_k: int = 5) -> List[RankedProduct]:
    ranked: List[Tuple[float, RankedProduct]] = []

    for p in products:
        score = 0.0
        reasons: List[str] = []
        tradeoffs: List[str] = []

        price = p.price_gbp
        rating = p.rating
        ship = p.shipping_days

        ram = int(p.attributes.get("ram_gb", 0))
        storage = int(p.attributes.get("storage_gb", 0))
        battery = float(p.attributes.get("battery_hours", 0))
        weight = float(p.attributes.get("weight_kg", 999))

        if c.max_price_gbp is not None:
            if price <= c.max_price_gbp:
                score += 2.0
                reasons.append(f"Within budget (£{price:.2f} ≤ £{c.max_price_gbp:.2f}).")
            else:
                score -= 3.0
                tradeoffs.append("Over budget.")

        if c.min_ram_gb is not None:
            if ram >= c.min_ram_gb:
                score += 1.5
                reasons.append(f"Meets RAM need ({ram}GB).")
            else:
                score -= 2.5
                tradeoffs.append(f"Lower RAM ({ram}GB).")

        if c.min_battery_hours is not None:
            if battery >= c.min_battery_hours:
                score += 1.2
                reasons.append(f"Good battery ({battery}h).")
            else:
                score -= 1.5
                tradeoffs.append(f"Weaker battery ({battery}h).")

        if c.max_weight_kg is not None:
            if weight <= c.max_weight_kg:
                score += 0.8
                reasons.append(f"Lightweight ({weight}kg).")
            else:
                score -= 1.0
                tradeoffs.append(f"Heavier ({weight}kg).")

        score += (rating - 3.5) * 1.2
        if rating >= 4.5:
            reasons.append(f"Highly rated ({rating}/5).")

        score += max(0.0, (8 - ship)) * 0.12
        if ship <= 2:
            reasons.append(f"Fast delivery ({ship} days).")
        elif ship >= 6:
            tradeoffs.append(f"Slower delivery ({ship} days).")

        if c.max_price_gbp is not None and price <= c.max_price_gbp:
            score += (c.max_price_gbp - price) / max(c.max_price_gbp, 1.0) * 0.6

        rp = RankedProduct(product=p, score=round(score, 3), reasons=reasons[:4], tradeoffs=tradeoffs[:3])
        ranked.append((score, rp))

    ranked.sort(key=lambda x: x[0], reverse=True)
    return [rp for _, rp in ranked[:top_k]]
