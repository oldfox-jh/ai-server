import os
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from pathlib import Path
from entity.rag import RagRequest

router = APIRouter(
    prefix="/rags",
    tags=["rags"],
    responses={404: {"description": "Not found"}},
)

@router.get("/list")
async def register_document():
    # file이 있을 경우 처리


    return {"op": "rag"}

@router.post("/list")
async def register_document(data: RagRequest= Depends(), file: UploadFile | None = File(None)):
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

        except Exception as e:
            return JSONResponse(content={"message": f"파일 업로드 중 오류 발생: {e}"}, status_code=500)

    return {"op": "rag"}

@router.post("/register")
async def register_document(data: RagRequest= Depends(), file: UploadFile | None = File(None)):
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

        except Exception as e:
            return JSONResponse(content={"message": f"파일 업로드 중 오류 발생: {e}"}, status_code=500)

    return {"op": "rag"}