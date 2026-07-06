import os
from typing import Optional

from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from pathlib import Path
from util.ocr.pdf_process import DoclingProcess
from util.ocr.image_process import VLMProcess
from util.rag.tokenizer_service import TokenizerService
import db.rag as db

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
async def register_document(query: str, file: UploadFile | None = File(None)):
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
async def register_document(user_uuid: str, message_uuid: Optional[str] = None, file: UploadFile | None = File(None)):
    str_result = ""
    file_uuid = ""
    document_uuid = ""

    # file이 있을 경우 처리
    if file:
        try:
            # 파일 저장
            date_string = datetime.now().strftime("%Y%m%d")
            if os.getenv("DEBUG"):
                file_location = os.path.join(os.getenv("DEBUG_UPLOAD_FOLDER"), date_string, file.filename)
                folder_path = Path(os.path.join(os.getenv("DEBUG_UPLOAD_FOLDER"), date_string))
            else:
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
                "type": file.content_type,
            }

            # 파일에서 텍스트 추출
            process = None
            file_type = None
            # pdf 추출
            if Path(file_location).suffix.lower() == ".pdf":
                process = DoclingProcess()
                file_type = "pdf"
            # 이미지 추출
            elif Path(file_location).suffix.lower() == ".png" or Path(file_location).suffix.lower() == ".jpg" or Path(file_location).suffix.lower() == ".jpeg":
                process = VLMProcess()
                file_type = "image"

            # text-chunk
            if process:
                str_result = process.start(file_location)

            # 파일 정보 db에 추가..
            uuids = db.add_document(user_uuid, message_uuid, file_info["filename"], file_info["type"], file_location, file_info["size"])
            document_uuid = uuids[0] if uuids else None
            file_uuid = uuids[1] if uuids else None

            print(file_uuid)

        except Exception as e:
            return JSONResponse(content={"message": f"파일 업로드 중 오류 발생: {e}"}, status_code=500)

        chunks = TokenizerService().recursive_split_text(str_result)

        for i, text_segment in enumerate(chunks):
            # 임베딩해서 데이터 db에 적재
            db.add_chunk(document_uuid, i, text_segment)

    return {"text": str_result}

"""
    등록된 파일 정보 삭제, rag 데이터 있으면 같이 삭제
"""
@router.post("/delete")
async def delete_document(file_uuid:str):
    # file이 있을 경우 처리


    return {"op": "rag"}