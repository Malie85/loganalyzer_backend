from fastapi import APIRouter, Depends, HTTPException, status, Response,UploadFile,File, Cookie, Request
from sqlalchemy.orm import Session
import os
import secrets
from db.database import get_db
from models import files as files_model
from services.check_coockie import check_coockie

MAX_FILE_SIZE = 50 * 1024 * 1024
CHUNK_SIZE = 1 * 1024 * 1024
MAX_REQUEST_SIZE = MAX_FILE_SIZE + 1 * 1024 * 1024

upload_router = APIRouter()

uploadDIR = "uploads"
os.makedirs(uploadDIR, exist_ok=True)

@upload_router.post(
    "/api/upload",
    status_code=status.HTTP_201_CREATED
)
def upload_file(request: Request, uploaded_file : UploadFile = File(...),session_id: str | None = Cookie(default=None), db: Session= Depends(get_db)):

    content_length = request.headers.get("content-length")

    if content_length is not None:
        try:
            request_size = int(content_length)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid Content-Length header",
            )

        if request_size < 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid Content-Length header",
            )

        if request_size > MAX_REQUEST_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail="Request is too large",
            )


    user_query_by_session,session_id_query = check_coockie(session_id,db)


    storage_key = secrets.token_urlsafe(32)

    path = os.path.join(uploadDIR,storage_key)

    total_size = 0

    try:
        with open(path, "wb") as destination:
            while True:
                chunk = uploaded_file.file.read(CHUNK_SIZE)

                if not chunk:
                    break

                total_size += len(chunk)

                # جلوگیری از عبور حجم واقعی فایل از سقف مجاز
                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        detail="File exceeds the 50 MiB limit",
                    )

                destination.write(chunk)

        new_file = files_model.files(
            originalName=uploaded_file.filename,
            fileOwner=user_query_by_session.id,
            storageKey=storage_key,
        )

        db.add(new_file)
        db.commit()

        return {
            "message": "Upload successful",
            "size": total_size,
        }

    except Exception:
        # حذف فایل ناقص یا فایلی که ثبت آن در دیتابیس شکست خورده
        if os.path.exists(path):
            os.remove(path)

        db.rollback()
        raise

    finally:
        uploaded_file.close()
    # with open(path, "wb") as f:
    #     f.write(file_contents)

    # new_file = files_model.files(
    #     originalName = uploaded_file.filename,
    #     fileOwner = user_query_by_session.id,
    #     storageKey = storge_key
    #     )
    
    # db.add(new_file)
    # db.commit()
    # return {"message": "upload Successfully"}

    
    

