def calculate_compound_savings(monthly_contribution, annual_rate_percent, months):
    monthly_rate = annual_rate_percent / 12 / 100
    total = 0.0

    for month in range(1, months + 1):
        total = (total + monthly_contribution) * (1 + monthly_rate)

    return total

# Пример использования:
X = float(input("Сколько откладываешь каждый месяц (X): "))
Y = float(input("Процент годовых (Y): "))
Z = int(input("На сколько месяцев (Z): "))

result = calculate_compound_savings(X, Y, Z)
print(f"Итоговая сумма через {Z} месяцев: {result:.2f} рублей")
