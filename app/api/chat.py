from fastapi import APIRouter
from app.agent.schemas import ChatRequest, AgentResponse
from app.agent.controller import handle_chat

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=AgentResponse)
def chat(body: ChatRequest):
    return handle_chat(body)
