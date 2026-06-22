from pydantic import BaseModel, Field

class ChatbotRequest(BaseModel):
    chatbot_uuid: str = Field(None, description="챗봇 모델 관리 번호")
    chatbot_name:str = Field(..., description="챗봇의 이름 (필수)")
    description:str = Field(None, description="챗봇에 대한 설명 (필수)")
    model_provider:str = Field(..., description="모델 제공 기업 (필수)")
    model_name:str = Field(..., description="모델의 이름 (필수)")
    system_prompt:str = Field(..., description="시스템 프롬프트 (필수)")
    temperature:float = Field(..., description="챗봇의 답변의 정확성 낮을 수록 보수적인 대답을 함 (필수)")
    max_tokens:int = Field(..., description="챗봇 최대 토큰값 (필수)")
    url: str = Field(..., description="챗봇 접속 주소 (필수)")


