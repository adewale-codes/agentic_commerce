from app.agent.schemas import ChatRequest, AgentResponse, CartItem
from app.agent.reasoning import extract_constraints, clarifying_questions
from app.services.catalog import search_products
from app.services.ranking import rank_products
from app.services.cart import create_cart

def handle_chat(req: ChatRequest) -> AgentResponse:
    c = extract_constraints(req.message)
    qs = clarifying_questions(c)

    if qs:
        return AgentResponse(
            type="questions",
            questions=qs,
            constraints=c,
            assistant_message="Quick questions so I can pick the best options for you."
        )

    candidates = search_products(query=req.message, c=c, limit=50)
    ranked = rank_products(candidates, c=c, top_k=5)

    if not ranked:
        return AgentResponse(
            type="recommendations",
            constraints=c,
            recommendations=[],
            cart=None,
            assistant_message="I couldn’t find matches with those constraints. Try increasing budget or relaxing a spec (like RAM or shipping)."
        )

    top_product_id = ranked[0].product.id
    cart = create_cart(user_id=req.user_id, items=[CartItem(product_id=top_product_id, quantity=1)])

    msg = (
        "Here are my top picks based on your requirements. "
        "I’ve also created a draft cart with the best match — you can approve it when ready."
    )

    return AgentResponse(
        type="recommendations",
        constraints=c,
        recommendations=ranked,
        cart=cart,
        assistant_message=msg
    )
