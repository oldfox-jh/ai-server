from fastapi import APIRouter
import db.chatbots as chatbot
from entity.chatbot import ChatbotRequest
from entity.common_response import CommonApiResponse

router = APIRouter(
    prefix="/chatbots",
    tags=["chatbots"],
    responses={404: {"description": "Not found"}},
)

"""
    챗봇 목록
"""
@router.get("/")
async def read_items():
    # 챗봇 목록
    return chatbot.list_chatbot_model()


"""
    챗봇 목록 검색
"""
@router.post("/")
async def read_items_with_condition():
    # 챗봇 검색
    return {"op": "chat"}

"""
    챗봇 모델 추가
"""
@router.post("/create")
async def create(data: ChatbotRequest):
    return chatbot.create_chatbot_model(data)
