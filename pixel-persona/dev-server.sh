#!/bin/bash

# Скрипт запуска разработческого сервера для PixelPersona

echo "Запуск разработческого сервера PixelPersona..."

# Проверка наличия node.js
if ! command -v node &> /dev/null
then
    echo "Node.js не найден. Пожалуйста, установите Node.js перед запуском сервера."
    exit 1
fi

# Создание временной директории для статических файлов
STATIC_DIR="/tmp/pixel-persona-dev"
mkdir -p "$STATIC_DIR"

# Копирование HTML файла в временную директорию
cp src/js/src/main/resources/index.html "$STATIC_DIR/"

# Запуск sbt в режиме отслеживания изменений
echo "Запуск sbt в режиме отслеживания изменений..."
echo "Откройте в браузере: http://localhost:8080"
echo "Нажмите Ctrl+C для остановки сервера"

# Используем встроенный HTTP сервер Node.js
cd "$STATIC_DIR"
npx http-server -p 8080 -c-1
