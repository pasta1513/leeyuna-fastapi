from pathlib import Path
import uuid
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.config import ALLOWED_EXTS, EXT_ALIAS, UPLOAD_DIR
from models.file_model import File

def get_ext_folder(filename: str | None) -> str | None:
    if not filename:
        return None

    ext = Path(filename).suffix.lower().lstrip('.')
    ext = EXT_ALIAS.get(ext, ext)

    if ext not in ALLOWED_EXTS:
        return None

    return ext

def save_file(upload: UploadFile, ext: str, db: Session) -> File | None:
    original_name = Path(upload.filename).name

    exist = (
        db.query(File)
            .filter(File.original_name == original_name)
            .first()
    )

    if exist:
        return None

    stored_name = f'{uuid.uuid4().hex}.{ext}'
    dest = UPLOAD_DIR / ext / stored_name
    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        with dest.open('wb') as f:
            shutil.copyfileobj(upload.file, f)

        file = File(
            original_name = original_name,
            stored_name = stored_name,
            ext = ext,
            path = f'{ext}/{stored_name}',
            size = dest.stat().st_size,
            content_type = upload.content_type
        )
        db.add(file)
        db.commit()
    except IntegrityError:
        db.rollback()
        dest.unlink(missing_ok=True)
        return None
    except Exception:
        db.rollback()
        dest.unlink(missing_ok=True)
        raise

    db.refresh(file)
    return file

def get_files(db: Session) -> list[File]:
    return (
        db.query(File)
            .order_by(File.id.desc()) # 최근 업로드 순
            .all()
    )

def get_download(filename: str, db: Session) -> tuple[File, Path] | None:
    file = (
        db.query(File)
            .filter(File.original_name == filename)
            .first()
    )

    if file is None:
        return None

    path = UPLOAD_DIR / file.path

    if not path.is_file():
        return None

    return file, path

