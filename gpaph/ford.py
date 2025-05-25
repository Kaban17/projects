def bellman_ford(edges, n_vertices, start):
    INF = float('inf')
    dist = [INF] * (n_vertices + 1)
    pred = [None] * (n_vertices + 1)

    dist[start] = 0

    for _ in range(n_vertices - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u

    # Восстановление пути
    def get_path(end):
        path = []
        while end is not None:
            path.append(end)
            end = pred[end]
        return list(reversed(path))

    return dist, get_path

# Ребра в формате (откуда, куда, вес)
edges = [
    (1, 2, 7),
    (1, 3, 5),
    (1, 5, 9),
    (2, 3, -8),
    (2, 4, 4),
    (3, 4, 3),
    (3, 5, 6),
    (4, 6, 8),
    (5, 4, -4),
    (5, 6, 6)
]

# Запускаем алгоритм
n_vertices = 6
start = 1
target = 6

distances, path_fn = bellman_ford(edges, n_vertices, start)

print(f"Минимальное расстояние от x₁ до x₆: {distances[target]}")
print("Путь:", " → ".join(f"x{v}" for v in path_fn(target)))

