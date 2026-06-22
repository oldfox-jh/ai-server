from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    chatbot_uuid : str = Field(..., description="챗봇 모델 관리 번호")
    content :str = Field(..., description="챗봇의 이름 (필수)")
    user_uuid :str = Field(..., description="챗봇에 대한 설명 (필수)")
    message_uuid :str = Field(..., description="모델 제공 기업 (필수)")


