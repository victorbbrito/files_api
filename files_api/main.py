from typing import List

from files_api import models
from files_api.database import engine
from files_api.database import get_db
from files_api.services import save_file
from files_api.services import get_file_by_id

from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi import UploadFile

from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title= "Upload Files")

# Rota para upload de arquivos
@app.post("/upload-file/")
async def upload_file(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    file_urls = []
    for file in files:
        try:
            file_url = save_file(file, db)
            file_urls.append(file_url)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"File upload failed: {str(e)}")
    
    return {"uploaded_files": file_urls}

@app.get("/download-file/{file_id}")
async def download_file_by_id(file_id: int, db: Session = Depends(get_db)):
    return get_file_by_id(file_id, db)