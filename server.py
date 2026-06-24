from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from routers import chat
from routers import chatbots
from routers import rags

from util.rag.tokenizer_service import TokenizerService

# 서버시작과 종료시 할일 처리
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 환경설정 로딩
    load_dotenv()

    # 토크나이저 초기화
    TokenizerService()

    yield

# FastAPI 서버 실행
app = FastAPI(lifespan=lifespan)

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(chat.router)
app.include_router(chatbots.router)
app.include_router(rags.router)



@app.get("/")
def read_root():
    return {"chat_url":  os.getenv("CHAT_BASE_URL")}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)