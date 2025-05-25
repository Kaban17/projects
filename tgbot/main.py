import asyncio
from handle_file import SRTProcess
from pathlib import Path
from handle_file import translate


async def main():
    # 1) Парсим и загружаем контент
    parser = SRTProcess.SubtitlesParser(path=Path("file.srt"))
    await parser.load_content()

    # 2) Обрабатываем весь файл, получаем cleaned_words
    processor = SRTProcess.AsyncTextProcessor()
    cleaned_words = await processor.process_chunk(parser.content)

    # 3) Переводим именно очищённые слова
    translations = await translate.translate_words(cleaned_words[:50])

    # 4) Берём статистику
    stats = processor.get_stats()

    # 5) Выводим всё, что нужно
    print("Очищённые слова:", cleaned_words[:10])
    print("Переводы:", translations)
    print(f"Всего слов обработано: {stats['total_words']}")
    print(f"Уникальных слов: {stats['unique_words']}")
    print("Топ-10 слов:", stats["top_words"])


if __name__ == "__main__":
    asyncio.run(main())
