from typing import Dict, List
from uuid import uuid4
from app.agent.schemas import Cart, CartItem, Product
from app.services.catalog import load_products

_carts: Dict[str, Cart] = {}

def _price_lookup(product_id: str) -> float:
    products = load_products()
    for p in products:
        if p.id == product_id:
            return float(p.price_gbp)
    raise ValueError(f"Unknown product_id: {product_id}")

def _recalc(cart: Cart) -> Cart:
    total = 0.0
    for it in cart.items:
        total += _price_lookup(it.product_id) * it.quantity
    cart.total_gbp = round(total, 2)
    return cart

def create_cart(user_id: str, items: List[CartItem]) -> Cart:
    cart_id = str(uuid4())
    cart = Cart(id=cart_id, user_id=user_id, status="draft", items=items)
    cart = _recalc(cart)
    _carts[cart_id] = cart
    return cart

def get_cart(cart_id: str) -> Cart:
    if cart_id not in _carts:
        raise KeyError("Cart not found")
    return _carts[cart_id]

def update_cart(cart_id: str, items: List[CartItem]) -> Cart:
    cart = get_cart(cart_id)
    if cart.status != "draft":
        raise ValueError("Cart is not editable after approval")
    cart.items = items
    cart = _recalc(cart)
    _carts[cart_id] = cart
    return cart

def approve_cart(cart_id: str) -> Cart:
    cart = get_cart(cart_id)
    cart.status = "approved"
    _carts[cart_id] = cart
    return cart
