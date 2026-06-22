from fastapi import APIRouter, File, UploadFile, Depends
import os
from openai import OpenAI
from typing import cast, Any
from fastapi.responses import JSONResponse
from datetime import datetime
from pathlib import Path
from entity.chat import ChatRequest
import db.chatbots as chatbot

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

"""
    대화 요청(텍스트만)
"""
@router.post("/")
async def chat( data: ChatRequest= Depends(), file: UploadFile | None = File(None)):
    # 챗봇 모델정보 가져오기
    bot = chatbot.chatbot_model(data)
    # bot 정보가 없을 경우
    if bot is None:
        bot = {
            "url": os.getenv("CHAT_BASE_URL"),
            "temperature": 0.2,
            "max_tokens": 2048,
            "model_name": os.getenv("CHAT_MODEL_NAME"),
            "system_prompt": "# 역할 "
                             "너는 유용하고, 친절하며, 정직한 AI 어시스턴트야. 사용자의 질문에 명확하고 이해하기 쉽게 답변해야 해."
                             ""
                             "# 규칙"
                             "- 항상 예의 바르고 존댓말(해요체)을 사용해 줘."
                             "- 복잡한 개념은 단계를 나누어 번호(1., 2., 3.)나 불릿 포인트(*)로 깔끔하게 정리해 줘."
                             "- 모르는 정보나 확실하지 않은 사실은 억지로 지어내지 말고, 잘 모른다고 솔직하게 답변해야 해 (할루시네이션 방지)."
                             "- 가급적 3줄~5줄 내외로 간결하게 핵심만 먼저 말하고, 필요한 경우 부연 설명을 붙여줘."
        }

    # 챗볼 질문 작성
    _messages = [  # type: ignore
        {
            "role": "system",
            "content": str(bot["system_prompt"])
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"{data.content}"
                },
            ],
        }
    ]

    # file이 있을 경우 처리
    if file:
        try:
            # 파일 저장
            date_string = datetime.now().strftime("%Y%m%d")

            file_location = os.path.join(os.getenv("UPLOAD_FOLDER"), date_string, file.filename)
            folder_path = Path(os.path.join(os.getenv("UPLOAD_FOLDER"), date_string))

            # 폴더가 없으면 생성 (exist_ok=True는 이미 폴더가 있어도 에러를 내지 않는 옵션)
            folder_path.mkdir(parents=True, exist_ok=True)

            with open(file_location, 'wb+') as file_object:
                file_object.write(file.file.read())

            # 파일 정보 반환
            file_size = os.path.getsize(file_location)
            file_info = {
                "filename": file.filename,
                "size": file_size,
                "content_type": file.content_type,
            }
            # 파일 정보 db에 추가..

            # 파일 데이터 질문에 추가함.
            user_content = _messages[1]["content"]
            # 안전하게 '리스트' 타입이 맞을 때만 append 실행
            if isinstance(user_content, list):
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"{"test"}"
                    },
                })

        except Exception as e:
            return JSONResponse(content={"message": f"파일 업로드 중 오류 발생: {e}"}, status_code=500)

    # OpenAI 라이브러리를 이용해서 질문 시작
    llm = OpenAI(
        api_key="vllm",
        base_url=bot["url"],
    )

    response = llm.chat.completions.create(
        model=bot["model_name"],
        messages=cast(Any, _messages),
        max_tokens=2048,
        temperature=0.2,
    )

    result_text = " " + response.choices[0].message.content

    return {"chat":result_text}