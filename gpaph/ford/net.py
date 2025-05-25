import networkx as nx
import matplotlib.pyplot as plt

# Данные: {Работа: (предшественники, длительность)}
data = {
    1: ([], 10),
    2: ([], 12),
    3: ([1], 14),
    4: ([1, 2], 11),
    5: ([1, 2], 7),
    6: ([1, 4], 9),
    7: ([3], 15),
    8: ([1, 4], 13),
    9: ([5, 6], 8)
}

# Создаём граф
G = nx.DiGraph()

# Добавляем работы и зависимости
for task, (deps, duration) in data.items():
    G.add_node(task, duration=duration)
    for dep in deps:
        G.add_edge(dep, task)

# Визуализация графа
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', arrows=True)
plt.title("Сетевой график работ")
plt.show()

# Расчёт ранних сроков (forward pass)
early_start = {task: 0 for task in data}
early_finish = {}

for task in nx.topological_sort(G):
    max_prev_finish = max([early_finish.get(dep, 0) for dep in G.predecessors(task)], default=0)
    early_start[task] = max_prev_finish
    early_finish[task] = early_start[task] + G.nodes[task]['duration']

total_duration = max(early_finish.values())

# Расчёт поздних сроков (backward pass)
late_finish = {task: total_duration for task in data}
late_start = {}

for task in reversed(list(nx.topological_sort(G))):
    min_next_start = min([late_start.get(succ, total_duration) for succ in G.successors(task)], default=total_duration)
    late_finish[task] = min_next_start
    late_start[task] = late_finish[task] - G.nodes[task]['duration']

# Расчёт резервов
total_float = {task: late_finish[task] - early_finish[task] for task in data}
free_float = {}
for task in data:
    if G.successors(task):
        free_float[task] = min([early_start[succ] for succ in G.successors(task)]) - early_finish[task]
    else:
        free_float[task] = 0

# Критический путь (работы с нулевым резервом)
critical_path = [task for task in data if total_float[task] == 0]

# Вывод результатов
print("Ранние сроки:")
for task in data:
    print(f"Работа {task}: РН = {early_start[task]}, РО = {early_finish[task]}")

print("\nПоздние сроки:")
for task in data:
    print(f"Работа {task}: ПН = {late_start[task]}, ПО = {late_finish[task]}")

print("\nРезервы времени:")
for task in data:
    print(f"Работа {task}: Полный резерв = {total_float[task]}, Свободный резерв = {free_float[task]}")

print("\nКритический путь:", critical_path)
print("Общая длительность проекта:", total_duration)
