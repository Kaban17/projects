from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import shutil
from pathlib import Path

app = FastAPI()

# Директория для загрузок
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Эндпоинт для загрузки файла
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Создаем путь для сохранения файла
        file_path = UPLOAD_DIR / file.filename

        # Сохраняем файл на диск
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "download_url": f"/files/{file.filename}"
        }
    finally:
        # Всегда закрываем файловый объект
        file.file.close()

# Эндпоинт для скачивания файла
@app.get("/files/{filename}")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename

    # Проверка существования файла
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Защита от Path Traversal атак
    if not file_path.resolve().parent == UPLOAD_DIR.resolve():
        raise HTTPException(status_code=403, detail="Access denied")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

# Эндпоинт для списка файлов
@app.get("/files/")
async def list_files():
    files = [f.name for f in UPLOAD_DIR.iterdir() if f.is_file()]
    return {"files": files}
