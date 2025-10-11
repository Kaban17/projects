#!/bin/bash
# --- КОНФИГУРАЦИЯ ---
# Референсный файл (Исходник, 1080p)
REFERENCE_FILE="big_buck_bunny_1080p24.y4m"
# Разрешение референса (для масштабирования искаженных видео)
REFERENCE_RESOLUTION="1920:1080"
# Количество потоков для VMAF (настройте под свой CPU)
THREADS=8
# Файл для сохранения финальных данных
RESULTS_CSV="vmaf_results.csv"
# --------------------

# Проверка наличия референсного файла
if [ ! -f "$REFERENCE_FILE" ]; then
    echo "Ошибка: Референсный файл '$REFERENCE_FILE' не найден."
    exit 1
fi

echo "--- Начинаем расчет VMAF ---"
echo "Референс: $REFERENCE_FILE"
echo "Потоков: $THREADS"
echo "Результаты будут сохранены в: $RESULTS_CSV"

# Создаем заголовок CSV-файла
echo "filename,bitrate_kbps,vmaf_score" > "$RESULTS_CSV"

# Цикл по всем MP4-файлам
for DISTORTED_FILE in bunny_*.mp4; do
    
    # Проверка, что файл существует (на случай, если нет совпадений)
    if [ ! -f "$DISTORTED_FILE" ]; then
        echo "Нет MP4 файлов для обработки"
        break
    fi
    
    # Создаем временный лог-файл VMAF
    LOG_FILE="${DISTORTED_FILE%.*}.json"
    
    echo "--- Обрабатываем: $DISTORTED_FILE ---"
    
    # 1. Расчет VMAF с масштабированием и многопоточностью
    # УБИРАЕМ 2>/dev/null чтобы видеть ошибки!
    ffmpeg -y -i "$DISTORTED_FILE" -i "$REFERENCE_FILE" \
    -filter_complex "[0:v]scale=${REFERENCE_RESOLUTION}[distorted];[distorted][1:v]libvmaf=log_path=${LOG_FILE}:log_fmt=json:n_subsample=1:n_threads=${THREADS}" \
    -f null -
    
    # Проверка, успешно ли прошел расчет VMAF
    if [ $? -ne 0 ]; then
        echo "!!! Ошибка выполнения ffmpeg для $DISTORTED_FILE !!!"
        continue
    fi
    
    # Даем время на запись файла
    sleep 1
    
    if [ ! -f "$LOG_FILE" ]; then
        echo "!!! JSON файл $LOG_FILE не создан. Пропускаем. !!!"
        continue
    fi
    
    # 2. Извлечение среднего VMAF из JSON
    if command -v jq &> /dev/null; then
        VMAF_SCORE=$(jq -r '.pooled_metrics.vmaf.mean // .["VMAF score"] // "N/A"' "$LOG_FILE" 2>/dev/null)
    else
        # Альтернатива без jq (менее надежная)
        VMAF_SCORE=$(grep -oP '"mean":\s*\K[0-9.]+' "$LOG_FILE" | head -1)
    fi
    
    if [ -z "$VMAF_SCORE" ] || [ "$VMAF_SCORE" = "N/A" ]; then
        echo "!!! Не удалось извлечь VMAF из $LOG_FILE !!!"
        VMAF_SCORE="N/A"
    fi
    
    # 3. Извлечение битрейта
    BITRATE_BPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 "$DISTORTED_FILE" 2>/dev/null)
    
    if [ -z "$BITRATE_BPS" ] || [ "$BITRATE_BPS" = "N/A" ]; then
        echo "!!! Не удалось получить битрейт для $DISTORTED_FILE. !!!"
        BITRATE_KBPS="N/A"
    else
        BITRATE_KBPS=$(echo "scale=0; $BITRATE_BPS / 1000" | bc 2>/dev/null)
    fi
    
    # 4. Запись результатов в CSV-файл
    echo "$DISTORTED_FILE,$BITRATE_KBPS,$VMAF_SCORE" >> "$RESULTS_CSV"
    
    
    echo "Готово. VMAF=$VMAF_SCORE, Битрейт=$BITRATE_KBPS kbps."
    echo ""
done

echo "--- Расчет завершен! ---"
echo "Данные готовы для построения графика в файле: $RESULTS_CSV"
