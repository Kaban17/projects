from itertools import permutations

word = "околоток"

# Общее количество уникальных перестановок
def count_unique_permutations(word):
    from math import factorial
    counter = {}
    for ch in word:
        counter[ch] = counter.get(ch, 0) + 1
    total = factorial(len(word))
    for count in counter.values():
        total //= factorial(count)
    return total

# Генерируем все перестановки и проверяем условие
valid_count = 0
seen = set()
for perm in permutations(word):
    perm_str = ''.join(perm)
    if perm_str not in seen:
        seen.add(perm_str)
        if 'ооо' not in perm_str:
            valid_count += 1

print(f"Количество подходящих перестановок: {valid_count}")
