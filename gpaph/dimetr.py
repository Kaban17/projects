from collections import defaultdict
class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        u_root = self.find(u)
        v_root = self.find(v)
        if u_root == v_root:
            return False
        if self.rank[u_root] < self.rank[v_root]:
            self.parent[u_root] = v_root
        else:
            self.parent[v_root] = u_root
            if self.rank[u_root] == self.rank[v_root]:
                self.rank[u_root] += 1
        return True

def kruskal(n, edges):
    dsu = DisjointSet(n)
    mst = []
    total_cost = 0

    edges.sort(key=lambda x: x[2])

    for u, v, w in edges:
        if dsu.union(u, v):
            mst.append((u, v, w))
            total_cost += w

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

# Добавим обратные рёбра для неориентированного графа
edges = []
for u, v, w in raw_edges:
    edges.append((u, v, w))
    edges.append((v, u, w))

# Найдем количество вершин (максимум среди номеров)
vertices = max(max(u, v) for u, v, w in edges)

mst, cost = kruskal(vertices, edges)
# Построение списка смежности для MST

def build_adjacency(mst):
    adj = defaultdict(list)
    for u, v, w in mst:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

def find_farthest(start, adj):
    max_dist = 0
    farthest_node = start
    visited = {}
    stack = [(start, 0)]
    while stack:
        node, dist = stack.pop()
        if node in visited:
            continue
        visited[node] = dist
        if dist > max_dist:
            max_dist = dist
            farthest_node = node
        for neighbor, weight in adj[node]:
            stack.append((neighbor, dist + weight))
    return max_dist, farthest_node, visited  # Возвращаем все расстояния

def compute_eccentricities(adj):
    eccentricities = {}
    distances = {}
    for node in adj:
        max_dist, farthest, visited = find_farthest(node, adj)
        eccentricities[node] = max_dist
        distances[node] = visited  # Сохраняем расстояния от каждой вершины
    return eccentricities, distances

# Вычисляем
adj = build_adjacency(mst)
eccentricities, all_distances = compute_eccentricities(adj)

# Находим радиус и соответствующие вершины
radius = min(eccentricities.values())
radius_nodes = [n for n, e in eccentricities.items() if e == radius]

# Находим диаметр и соответствующие вершины
diameter = max(eccentricities.values())
diameter_nodes = [n for n, e in eccentricities.items() if e == diameter]

# Находим конечные вершины диаметрального пути
_, end1, _ = find_farthest(1, adj)  # Произвольная стартовая точка
max_dist, end2, _ = find_farthest(end1, adj)  # Истинная конечная точка диаметра

print(f"Радиус: {radius}, достигается для вершин: {radius_nodes}")
print(f"Диаметр: {diameter}, достигается для вершин: {diameter_nodes}")
print(f"Диаметр образует путь между вершинами {end1} и {end2}")
print("\nЭксцентриситеты всех вершин:")
for node in sorted(eccentricities):
    print(f"Вершина {node}: {eccentricities[node]}")
