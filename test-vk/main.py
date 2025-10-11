import marimo

__generated_with = "0.15.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    # 1. Загрузка данных из CSV-файла
    try:
        df = pd.read_csv('vmaf_results.csv')
    except FileNotFoundError:
        print("Ошибка: Файл 'vmaf_results.csv' не найден. Убедитесь, что он находится в той же папке.")
        exit()

    # 2. Сортировка данных по оси X (Битрейту)
    # Это необходимо, чтобы точки на графике были соединены в правильном порядке.
    df = df.sort_values(by='bitrate_kbps')

    # 3. Построение графика
    plt.figure(figsize=(10, 6))

    # Построение основной линии VMAF (Битрейт на X, VMAF на Y)
    plt.plot(
        df['bitrate_kbps'], 
        df['vmaf_score'], 
        marker='o', # Точки для каждого видео
        linestyle='-', # Соединяем точки линией
        color='blue', 
        label='VMAF Score'
    )

    # 4. Добавление подписей к точкам
    for i, row in df.iterrows():
        # Используем разрешение как метку (удаляем расширение и 'bunny_')
        label = row['filename'].replace('bunny_', '').replace('.mp4', '') 
    
        # Добавляем текст: (X, Y), с небольшим смещением
        plt.annotate(
            label,
            (row['bitrate_kbps'] + 50, row['vmaf_score'] - 1), 
            fontsize=9
        )

    # 5. Настройка осей и заголовка
    plt.title('Кривая VMAF-Битрейт (Rate-Distortion Curve)')
    plt.xlabel('Битрейт (kbps)')
    plt.ylabel('Средний VMAF Score')

    # Установка диапазона оси Y от 0 до 100
    plt.ylim(0, 100)
    # Добавление сетки для лучшей читаемости
    plt.grid(True, linestyle='--', alpha=0.6)

    # 6. Сохранение и отображение графика
    plt.legend()
    plt.tight_layout() # Автоматическая подгонка макета
    plt.savefig('vmaf_bitrate_curve.png') # Сохранить график как PNG-файл
    plt.show() # Показать график на экране
    return


if __name__ == "__main__":
    app.run()
