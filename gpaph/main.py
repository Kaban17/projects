def find_paths_of_length_k(graph, start, k):
    paths = []

    def dfs(current, path):
        if len(path) == k + 1:  # k рёбер = k+1 вершина
            paths.append(path[:])
            return

        for neighbor in graph[current]:
            path.append(neighbor)
            dfs(neighbor, path)
            path.pop()

    dfs(start, [start])
    return paths

# Пример графа

subgraph = {
    1: [2, 4],
    2: [3, 6],
    3: [],
    4: [ 2],
    5: [1, 3],
    6: [ 5],
    7: [5],
    8: [4, 6,8, 9],
    9: []
}

k=0
for i in range(1,10):
    k+=len(find_paths_of_length_k(subgraph, i, 4))
print(k)
