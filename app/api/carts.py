from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.agent.schemas import Cart, CartItem
from app.services.cart import create_cart, get_cart, update_cart, approve_cart

router = APIRouter(prefix="/carts", tags=["carts"])

class CreateCartRequest(BaseModel):
    user_id: str
    items: List[CartItem]

class UpdateCartRequest(BaseModel):
    items: List[CartItem]

@router.post("", response_model=Cart)
def carts_create(body: CreateCartRequest):
    return create_cart(user_id=body.user_id, items=body.items)

@router.get("/{cart_id}", response_model=Cart)
def carts_get(cart_id: str):
    try:
        return get_cart(cart_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Cart not found")

@router.patch("/{cart_id}", response_model=Cart)
def carts_update(cart_id: str, body: UpdateCartRequest):
    try:
        return update_cart(cart_id, items=body.items)
    except KeyError:
        raise HTTPException(status_code=404, detail="Cart not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{cart_id}/approve", response_model=Cart)
def carts_approve(cart_id: str):
    try:
        return approve_cart(cart_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Cart not found")
