
INF = float('inf')

def prim(n, adj_matrix):
    selected = [False] * (n + 1)
    min_edge = [INF] * (n + 1)
    parent = [-1] * (n + 1)

    min_edge[1] = 0  # Начинаем с вершины 1
    total_cost = 0
    mst = []

    for _ in range(n):
        u = -1
        for v in range(1, n + 1):
            if not selected[v] and (u == -1 or min_edge[v] < min_edge[u]):
                u = v

        if min_edge[u] == INF:
            print("Граф несвязный!")
            return None

        selected[u] = True
        total_cost += min_edge[u]

        if parent[u] != -1:
            mst.append((parent[u], u, adj_matrix[parent[u]][u]))

        for v in range(1, n + 1):
            if adj_matrix[u][v] < min_edge[v] and not selected[v]:
                min_edge[v] = adj_matrix[u][v]
                parent[v] = u

    return mst, total_cost


# Входные данные
raw_edges = [
    (1, 2, 5), (1, 3, 6), (1, 4, 12), (1, 6, 5), (1, 10, 4),
    (2, 4, 9), (2, 5, 10), (2, 8, 7), (2, 9, 7), (2, 10, 9), (2, 11, 6),
    (3, 5, 3), (3, 7, 8), (3, 9, 8), (3, 12, 9),
    (4, 6, 5), (4, 8, 7), (4, 10, 4), (4, 11, 4), (4, 12, 6),
    (5, 6, 2), (5, 8, 7), (5, 10, 8), (5, 11, 13),
    (6, 7, 9), (6, 9, 10), (6, 12, 3),
    (7, 8, 5), (7, 10, 9), (7, 12, 4),
    (8, 9, 5), (8, 11, 6),
    (9, 11, 4),
    (10, 12, 3),
    (11, 12, 6)
]

# Построим матрицу смежности
n = 12  # количество вершин
adj_matrix = [[INF] * (n + 1) for _ in range(n + 1)]

for u, v, w in raw_edges:
    adj_matrix[u][v] = min(adj_matrix[u][v], w)
    adj_matrix[v][u] = min(adj_matrix[v][u], w)

# Запустим алгоритм Прима
mst, cost = prim(n, adj_matrix)

print("Минимальный остовной лес (алгоритм Прима):")
for u, v, w in mst:
    print(f"{u} - {v} : {w}")
print(f"Общая стоимость: {cost}")
