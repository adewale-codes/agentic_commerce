from pydantic import BaseModel, Field
from typing import Any, Optional, List, Literal, Dict

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    user_id: str = "demo_user"
    message: str
    history: List[ChatMessage] = Field(default_factory=list)

class Constraints(BaseModel):
    max_price_gbp: Optional[float] = None
    min_ram_gb: Optional[int] = None
    min_storage_gb: Optional[int] = None
    min_battery_hours: Optional[float] = None
    max_weight_kg: Optional[float] = None
    os: Optional[str] = None
    shipping_days_max: Optional[int] = None
    in_stock_only: bool = True

class ClarifyingQuestion(BaseModel):
    question: str
    choices: Optional[List[str]] = None

class Product(BaseModel):
    id: str
    title: str
    brand: str
    category: str
    price_gbp: float
    rating: float
    review_count: int
    shipping_days: int
    in_stock: bool
    attributes: Dict[str, Any]
    url: str

class RankedProduct(BaseModel):
    product: Product
    score: float
    reasons: List[str]
    tradeoffs: List[str]

class CartItem(BaseModel):
    product_id: str
    quantity: int = 1

class Cart(BaseModel):
    id: str
    user_id: str
    status: Literal["draft", "approved"] = "draft"
    items: List[CartItem] = Field(default_factory=list)
    total_gbp: float = 0.0

class AgentResponse(BaseModel):
    type: Literal["questions", "recommendations"]
    questions: Optional[List[ClarifyingQuestion]] = None
    constraints: Optional[Constraints] = None
    recommendations: Optional[List[RankedProduct]] = None
    cart: Optional[Cart] = None
    assistant_message: str
