#!/bin/bash

# --- КОНФИГУРАЦИЯ ---
INPUT_FILE="big_buck_bunny_1080p24.y4m"
OUTPUT_DIR="encoded_videos"
CUT_DURATION="00:00:30"  # Длительность обрезки (30 секунд)
CUT_START="00:00:00"     # Начало обрезки
# --------------------

# Проверка наличия входного файла
if [ ! -f "$INPUT_FILE" ]; then
    echo "Ошибка: Входной файл '$INPUT_FILE' не найден."
    exit 1
fi

# Создаем директорию для выходных файлов
mkdir -p "$OUTPUT_DIR"

echo "==================================="
echo "Начинаем обработку видео"
echo "Исходный файл: $INPUT_FILE"
echo "==================================="
echo ""

# Массив разрешений: название:ширина:высота
declare -a resolutions=(
    "1080p:1920:1080"
    "720p:1280:720"
    "480p:640:480"
    "360p:640:360"
    "240p:426:240"
    "144p:192:144"
)

# 1. Обрезаем видео (опционально)
echo "--- Шаг 1: Обрезка видео ---"
CUTTED_FILE="${OUTPUT_DIR}/cutted_bunny.y4m"

if [ -f "$CUTTED_FILE" ]; then
    echo "Обрезанный файл уже существует: $CUTTED_FILE"
    echo "Пропускаем обрезку."
else
    echo "Обрезаем первые $CUT_DURATION видео..."
    ffmpeg -i "$INPUT_FILE" -ss "$CUT_START" -t "$CUT_DURATION" -c copy "$CUTTED_FILE"
    
    if [ $? -eq 0 ]; then
        echo "✓ Обрезка завершена: $CUTTED_FILE"
    else
        echo "✗ Ошибка при обрезке видео"
        exit 1
    fi
fi
echo ""

# Используем обрезанное видео или оригинал
SOURCE_FILE="$INPUT_FILE"
# Если хотите использовать обрезанное видео, раскомментируйте:
# SOURCE_FILE="$CUTTED_FILE"

# 2. Кодируем в разные разрешения
echo "--- Шаг 2: Кодирование в разные разрешения ---"

for res_config in "${resolutions[@]}"; do
    # Разбираем конфигурацию
    IFS=':' read -r name width height <<< "$res_config"
    
    OUTPUT_FILE="${OUTPUT_DIR}/bunny_${name}.mp4"
    
    echo "Кодируем $name (${width}x${height})..."
    
    # Проверяем, существует ли уже файл
    if [ -f "$OUTPUT_FILE" ]; then
        echo "  Файл уже существует: $OUTPUT_FILE"
        echo "  Пропускаем."
        echo ""
        continue
    fi
    
    # Кодируем видео
    ffmpeg -i "$SOURCE_FILE" \
        -vf "scale=${width}:${height}" \
        -c:v libx264 \
        -preset medium \
        -crf 23 \
        -c:a copy \
        "$OUTPUT_FILE" 2>&1 | grep -E "frame=|error|Error"
    
    # Проверка успешности
    if [ $? -eq 0 ] && [ -f "$OUTPUT_FILE" ]; then
        # Получаем размер файла
        FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
        echo "  ✓ Готово: $OUTPUT_FILE (размер: $FILE_SIZE)"
    else
        echo "  ✗ Ошибка при кодировании $name"
    fi
    echo ""
done

echo "==================================="
echo "Обработка завершена!"
echo "==================================="
echo ""
echo "Результаты сохранены в: $OUTPUT_DIR/"
ls -lh "$OUTPUT_DIR"/*.mp4 2>/dev/null | awk '{print $9, "(" $5 ")"}'
