from pydantic import BaseModel, Field

class FileInfo(BaseModel):
    user_uuid: str = Field(..., description="파일 업로드한 사용자 관리번호(필수)")
    message_uuid:str = Field(None, description="대화 세션 관리번호 (필수)")
    file_name:str = Field(..., description="파일 명 (필수)")
    file_type:str = Field(..., description="파일 확장자 (필수)")
    save_path:str = Field(..., description="저장 경로 (필수)")
    file_size:str = Field(..., description="파일 크기 (필수)")


