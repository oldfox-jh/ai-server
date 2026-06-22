from pydantic import BaseModel, Field

class RagRequest(BaseModel):
    user_uuid :str = Field(..., description="파일 등록한 사용자 관리 키 (필수)")
    title :str = Field(..., description="파일 내용 제목 (필수)")