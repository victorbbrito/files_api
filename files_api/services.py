import os
import pandas as pd
from sqlalchemy.orm import Session
from fastapi import UploadFile
from .models import FileRecord
from fastapi import HTTPException
from fastapi.responses import FileResponse

UPLOAD_DIRECTORY = "uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def save_file(file: UploadFile, db: Session):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    
    # Salvar o arquivo no diretório
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # Registrar o arquivo no banco de dados
    file_record = FileRecord(
        file_name=file.filename,
        directory=file_location,
    )
    db.add(file_record)
    db.commit()
    db.refresh(file_record)
    
    return file_location

def process_file(file: UploadFile):
    # Verificar tipo do arquivo e carregá-lo no pandas
    if file.filename.endswith(".csv"):
        data = pd.read_csv(file.file)
    elif file.filename.endswith(".xlsx"):
        data = pd.read_excel(file.file, engine='openpyxl')
    else:
        raise ValueError("Unsupported file type")
    
    # Exemplo simples de processamento (retorna as 5 primeiras linhas)
    return data.head()

def get_file_by_id(file_id: int, db: Session):
    # Consultar o banco de dados pelo ID
    file_record = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    
    if file_record is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = file_record.directory
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    # Retornar o arquivo como resposta
    return FileResponse(file_path, media_type='application/octet-stream', filename=file_record.file_name)