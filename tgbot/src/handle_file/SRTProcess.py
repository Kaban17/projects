from collections import Counter
from functools import wraps
from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
import aiofiles
import asyncio
import nltk
import pysrt
import re
import time
import unicodedata

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f"Функция «{func.__name__}» выполнена за {elapsed:.6f} секунд")
        return result
    return wrapper

# Предзагрузка ресурсов синхронно
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('words', quiet=True)
nltk.download('stopwords', quiet=True)
from nltk.corpus import wordnet
wordnet.ensure_loaded()

class TextCleaner:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words('english'))
        self.vocab = set(words.words())

    async def clean_text(self, text: str) -> List[str]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self._sync_clean_text,
            text
        )

    def _sync_clean_text(self, text: str) -> List[str]:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
        text = re.sub(r'[^a-z\s]', ' ', text.lower())
        tokens = word_tokenize(text)

        filtered = []
        for word, tag in pos_tag(tokens):
            pos = tag[0].lower()
            pos = pos if pos in {'a', 'r', 'n', 'v'} else 'n'
            lemma = self.lemmatizer.lemmatize(word, pos)

            if (len(lemma) > 1 and
                lemma.isalpha() and
                lemma in self.vocab and
                lemma not in self.stopwords):
                filtered.append(lemma)

        return filtered

class AsyncTextProcessor:
    def __init__(self):
        self.counter = Counter()
        self.total = 0
        self.cleaner = TextCleaner()

    async def process_chunk(self, chunk: List[str]) -> List[str]:
        """
        Обрабатывает список строк и возвращает плоский список очищенных слов.
        Также обновляет счетчики внутри экземпляра.
        """
        tasks = [self.cleaner.clean_text(line) for line in chunk]
        results = await asyncio.gather(*tasks)

        # Плоский список всех слов из результатов
        flat_words = [word for words_list in results for word in words_list]

        # Обновление статистики
        self.counter.update(flat_words)
        self.total += len(flat_words)

        return flat_words

    async def process_file(self, file_path: Path, chunk_size: int = 100) -> List[str]:
        """
        Асинхронно читает файл, обрабатывает его по чанкам и возвращает
        полный список очищенных слов из всего файла.
        """
        all_words: List[str] = []

        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            chunk: List[str] = []
            async for line in f:
                chunk.append(line)
                if len(chunk) >= chunk_size:
                    chunk_words = await self.process_chunk(chunk)
                    all_words.extend(chunk_words)
                    chunk = []

            # Обработка остатка
            if chunk:
                chunk_words = await self.process_chunk(chunk)
                all_words.extend(chunk_words)

        return all_words

    def get_stats(self, top_n=100) -> dict:
        return {
            'total_words': self.total,
            'unique_words': len(self.counter),
            'top_words': self.counter.most_common(top_n)
        }

class SubtitlesParser(BaseModel):
    path: Path
    encoding: str = 'utf-8'
    content: Optional[List[str]] = None

    async def load_content(self) -> None:
        """Асинхронная загрузка и парсинг субтитров"""
        try:
            async with aiofiles.open(self.path, 'r', encoding=self.encoding) as f:
                content = await f.read()
        except UnicodeDecodeError:
            async with aiofiles.open(self.path, 'r', encoding='utf-8-sig') as f:
                content = await f.read()

        subs = pysrt.from_string(content)
        self.content = [
            ' '.join(sub.text.strip().split()).replace('\n', ' ')
            for sub in subs
            if sub.text.strip()
        ]

    async def create_translated_file(self, translations: dict, output_path: str):
        """Создает новый SRT-файл с переводами."""
        try:
            async with aiofiles.open(self.path, 'r', encoding=self.encoding) as f:
                content = await f.read()
        except UnicodeDecodeError:
            async with aiofiles.open(self.path, 'r', encoding='utf-8-sig') as f:
                content = await f.read()
        
        subs = pysrt.from_string(content)
        cleaner = TextCleaner()

        for sub in subs:
            cleaned_words = cleaner._sync_clean_text(sub.text)
            unique_words_in_sub = sorted(list(set(cleaned_words)))
            
            translation_lines = []
            current_line = ""
            for word in unique_words_in_sub:
                translation = translations.get(word)
                if translation and translation != word:
                    part = f"{word} - {translation}, "
                    if len(current_line) + len(part) > 80:
                        translation_lines.append(current_line.strip().strip(','))
                        current_line = part
                    else:
                        current_line += part
            
            if current_line:
                translation_lines.append(current_line.strip().strip(','))

            if translation_lines:
                sub.text += "\n" + "\n".join(translation_lines)

        # Сохранение файла должно быть синхронным, но в асинхронном контексте
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, subs.save, output_path, 'utf-8')
