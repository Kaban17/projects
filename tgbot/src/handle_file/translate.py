from googletrans import Translator
import asyncio

async def translate_word_async(word: str, target_lang: str='ru', src_lang: str = 'auto') -> str:
    translator = Translator()
    try:
        translation = await translator.translate(word, dest=target_lang, src=src_lang)
        return translation.text
    except Exception as e:
        return f"Ошибка перевода: {str(e)}"

async def translate_words(
    words: list[str],
    target_lang: str = 'ru',
    src_lang: str = 'auto'
) -> dict[str, str]:
    print("Translating words...")
    # 1) Собираем корутины в список
    tasks = [translate_word_async(w, target_lang, src_lang) for w in words]
    # 2) Ждём всех сразу
    translations = await asyncio.gather(*tasks)
    # 3) Формируем словарь
    return dict(zip(words, translations))
