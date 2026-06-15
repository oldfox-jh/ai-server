from fastapi import APIRouter

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items():
    return {"op": "chat"}