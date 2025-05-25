
from collections import defaultdict
import heapq

# Рёбра дерева
edges = [
    (1,2), (1,3), (1,4),
    (2,5),
    (3,6),
    (6,9),
    (4,7), (4,8),
    (7,10),
    (10,12),
    (8,11)
]

# Построим граф без весов
graph = defaultdict(set)
for u, v in edges:
    graph[u].add(v)
    graph[v].add(u)

# Множество вершин
nodes = set(graph.keys())

# Массив степеней
degree = {node: len(neighbors) for node, neighbors in graph.items()}

# Используем кучу для быстрого выбора минимального листа
leaves = []
for node in nodes:
    if degree[node] == 1:
        heapq.heappush(leaves, node)

# Строим код Прюфера
prufer = []
for _ in range(len(nodes) - 2):
    leaf = heapq.heappop(leaves)
    neighbor = next(iter(graph[leaf]))

    prufer.append(neighbor)
    print("Добавил в код прюфера", neighbor)
    # Удаляем ребро
    graph[neighbor].remove(leaf)
    degree[neighbor] -= 1
    if degree[neighbor] == 1:
        heapq.heappush(leaves, neighbor)

    del graph[leaf]  # Удаляем вершину полностью
    print("удалил вершину", leaf)

# Вывод
print("Код Прюфера:", prufer)
print(len(prufer))
