#!/bin/bash

# Скрипт сборки проекта PixelPersona

echo "Начало сборки проекта PixelPersona..."

# Проверка наличия sbt
if ! command -v sbt &> /dev/null
then
    echo "sbt не найден. Пожалуйста, установите sbt перед запуском сборки."
    exit 1
fi

# Очистка предыдущей сборки
echo "Очистка предыдущей сборки..."
sbt clean

# Компиляция проекта
echo "Компиляция проекта..."
sbt compile

# Запуск тестов
echo "Запуск тестов..."
sbt test

# Создание JavaScript бандла
echo "Создание JavaScript бандла..."
sbt fastOptJS

echo "Сборка завершена успешно!"
echo "Файлы сборки находятся в директории target/"
