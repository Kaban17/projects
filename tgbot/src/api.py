import asyncio
import os
from pathlib import Path
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from .handle_file.SRTProcess import SubtitlesParser, AsyncTextProcessor
from .handle_file.translate import translate_words

app = FastAPI()

PROCESSED_FILES_DIR = Path("processed_files")
PROCESSED_FILES_DIR.mkdir(exist_ok=True)

@app.post("/process-srt/")
async def process_srt_file(file: UploadFile = File(...)):
    """
    Принимает SRT-файл, обрабатывает его, сохраняет переведенную версию
    и возвращает статистику и ссылку на скачивание.
    """
    if not file.filename.endswith('.srt'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .srt file.")

    # Сохраняем загруженный файл во временное место
    temp_dir = Path("/tmp/srt_uploads")
    temp_dir.mkdir(exist_ok=True)
    temp_file_path = temp_dir / file.filename
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Парсинг и обработка
        parser = SubtitlesParser(path=temp_file_path)
        await parser.load_content()

        if not parser.content:
            raise HTTPException(status_code=400, detail="File seems to be empty or invalid.")

        processor = AsyncTextProcessor()
        # Обрабатываем контент, который уже в памяти
        all_words = await processor.process_chunk(parser.content)
        
        unique_words = list(set(all_words))
        
        # 2. Перевод
        translations = await translate_words(unique_words)
        
        # 3. Получение статистики
        stats = processor.get_stats(top_n=100)
        
        # 4. Создание нового файла с переводами
        output_filename = f"translated_{file.filename}"
        output_filepath = PROCESSED_FILES_DIR / output_filename
        
        await parser.create_translated_file(translations, str(output_filepath))

        # 5. Формирование ответа
        return {
            "message": "File processed successfully.",
            "statistics": stats,
            "download_url": f"/downloads/{output_filename}"
        }
    finally:
        # Очистка временного файла
        if temp_file_path.exists():
            os.remove(temp_file_path)

@app.get("/downloads/{filename}")
async def download_file(filename: str):
    """
    Отдает на скачивание обработанный файл.
    """
    file_path = PROCESSED_FILES_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    
    return FileResponse(
        path=file_path,
        media_type='application/octet-stream',
        filename=filename
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the SRT Subtitle Processor API. Use the /docs endpoint for more info."}
