from pathlib import Path
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from schemas.file_schema import FileInfo
from services import file_service
from connection import get_db

file_router = APIRouter(tags=['File'])

@file_router.post('',
                  response_model=FileInfo,
                  status_code=status.HTTP_201_CREATED)
def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    ext = file_service.get_ext_folder(file.filename)

    if ext is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='허용되지 않는 확장자입니다.'
        )

    if len(Path(file.filename).name) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='파일명이 너무 깁니다.'
        )

    saved = file_service.save_file(file, ext, db)

    if saved is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='이미 같은 이름의 파일이 있습니다.'
        )

    return saved

@file_router.get('', response_model=list[FileInfo])
def get_files(db: Session = Depends(get_db)):
    return file_service.get_files(db)

@file_router.get('/{filename}')
def download_file(filename: str, db: Session = Depends(get_db)):
    result = file_service.get_download(filename, db)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='존재하지 않는 파일입니다.'
        )

    file, path = result
    return FileResponse(path, filename=file.original_name)

