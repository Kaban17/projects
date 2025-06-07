Задание: "Универсальный конвертер данных"
Цель:

Создать систему для конвертации между разными форматами данных (JSON, XML, YAML) с использованием дженериков для обработки различных типов структур и интерфейсов для универсального доступа.

Требования:

    Интерфейс Converter:

go

type Converter interface {
    Convert(data []byte) ([]byte, error)
}

    Дженерик-структуры для форматов:

go

type JSONHandler[T any] struct{...}
type XMLHandler[T any] struct{...}
type YAMLHandler[T any] struct{...}

    Методы обработки:

    Каждая структура должна реализовывать Convert() для преобразования в другой формат

    Использовать дженерики для работы с любым типом данных T

    Фабрика конвертеров:

go

func NewConverter[T any](inputFormat, outputFormat string) (Converter, error) {...}

Детали реализации:

    Конвертеры должны поддерживать:

go

// JSON → XML
// JSON → YAML
// XML → JSON
// YAML → JSON

    Пример структур данных:

go

type User struct {
    ID   int    `json:"id" xml:"id" yaml:"id"`
    Name string `json:"name" xml:"name" yaml:"name"`
}

type Product struct {
    SKU  string  `json:"sku" xml:"sku" yaml:"sku"`
    Cost float64 `json:"cost" xml:"cost" yaml:"cost"`
}

    Реализация Convert():

go

func (j *JSONHandler[T]) Convert(data []byte) ([]byte, error) {
    var obj T
    if err := json.Unmarshal(data, &obj); err != nil {
        return nil, err
    }
    // Конвертация в целевой формат (XML/YAML)
}

Пример использования:
go

// Конвертация User из JSON в XML
converter, _ := NewConverter[User]("json", "xml")
jsonData := []byte(`{"id":1,"name":"John"}`)

xmlData, err := converter.Convert(jsonData)
// Результат: <User><id>1</id><name>John</name></User>

// Конвертация Product из YAML в JSON
converter, _ := NewConverter[Product]("yaml", "json")
yamlData := []byte(`
sku: "123-ABC"
cost: 19.99
`)

jsonData, err := converter.Convert(yamlData)
// Результат: {"sku":"123-ABC","cost":19.99}

Критерии выполнения:

    Поддержка минимум 3 форматов данных

    Использование дженериков для типа T

    Реализация интерфейса Converter

    Обработка ошибок:

        Неподдерживаемые форматы

        Невалидные входные данные

        Ошибки маршаллинга/анмаршаллинга

    Юнит-тесты для:

        Всех вариантов конвертации

        Разных типов структур

        Ошибочных сценариев

Технические требования:

    Использовать стандартные библиотеки:

        encoding/json

        encoding/xml

        gopkg.in/yaml.v3 (можно добавить как зависимость)

    Для фабрики использовать pattern-matching на строки форматов

    Дженерик-структуры до

    лжны содержать информацию о целевом формате

Это задание развивает:

    Работу с дженериками для различных структур

    Реализацию интерфейсов

    Обработку разных форматов данных

    Паттерн "Фабрика"

    Маршаллинг/анмаршаллинг данных

    Обработку ошибок
