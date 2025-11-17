# Руководство по разработке PixelPersona

## Настройка окружения

### Требуемые инструменты

1. **Java Development Kit (JDK) 11 или выше**
   - Рекомендуется использовать OpenJDK
   - Убедитесь, что переменная окружения JAVA_HOME указывает на установленный JDK

2. **sbt (Simple Build Tool) 1.9.0 или выше**
   - Следуйте инструкциям на официальном сайте sbt: https://www.scala-sbt.org/download.html

3. **Node.js (для разработческого сервера)**
   - Версия 14 или выше
   - Установите с https://nodejs.org/

### Импорт проекта в IDE

Проект может быть импортирован в любую IDE, поддерживающую Scala и sbt:
- IntelliJ IDEA с плагином Scala
- VS Code с Metals
- Emacs с ENSIME

## Структура кода

### Общая архитектура

PixelPersona использует архитектуру shared cross-platform project:
- `shared` - общий код между JVM и JS
- `jvm` - серверный код (потенциально для API)
- `js` - клиентский код (фронтенд)

### Основные компоненты

1. **AvatarGenerator** - генерация аватаров по имени
2. **AsciiArtGenerator** - преобразование изображений в ASCII-арт
3. **Exporter** - экспорт в различные форматы
4. **ImageProcessor** - обработка изображений