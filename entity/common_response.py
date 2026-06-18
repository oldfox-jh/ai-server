from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar

# 어떤 데이터 구조든 담을 수 있도록 제네릭 선언
T = TypeVar('T')

class CommonApiResponse(BaseModel, Generic[T]):
    success:bool = False
    message:str = "요청이 성공적으로 처리되었습니다."
    code:Optional[str] = "SUCCESS"
    data: Optional[T] = None
    detail:Optional[str] = None