from fastapi import APIRouter

router = APIRouter(
    prefix="/rags",
    tags=["rags"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items():
    return {"op": "rag"}