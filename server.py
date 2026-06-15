from fastapi import FastAPI
from routers import chats
from routers import rags
app = FastAPI()

# 라우터 등록
app.include_router(chats.router)
app.include_router(rags.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}