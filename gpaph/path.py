
import numpy as np

# Вершины подграфа
nodes = list(range(1, 10))  # Вершины 1-9
node_index = {node: i for i, node in enumerate(nodes)}  # отображение: вершина -> индекс в матрице

# Подграф
subgraph = {
    1: [2, 4, 5],
    2: [1, 3, 4, 6],
    3: [2, 5],
    4: [1, 2, 8],
    5: [1, 3, 6, 7],
    6: [2, 5, 8],
    7: [5, 8],
    8: [4, 6,8, 9],
    9: [8]
}

# Построение матрицы смежности
n = len(nodes)
adj_matrix = np.zeros((n, n), dtype=int)

for u in subgraph:
    for v in subgraph[u]:
        i, j = node_index[u], node_index[v]
        adj_matrix[i][j] = 1

# Возведение матрицы в степень 3
adj_matrix_cubed = np.linalg.matrix_power(adj_matrix, 3)

# Подсчет общего количества путей длины 3
total_paths_len_3 = np.sum(adj_matrix_cubed)
print(adj_matrix, total_paths_len_3)
