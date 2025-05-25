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

print("Минимальный остовной лес:")
for u, v, w in mst:
    print(f"{u} - {v} : {w}")
print(f"Общая стоимость: {cost}")

import heapq

# Build adjacency list
adj = {}
for u, v, w in mst:
    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))

def dijkstra(start):
    dist = {node: float('inf') for node in adj}
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist

# Compute eccentricities
eccentricities = {}
for node in sorted(adj):
    dist = dijkstra(node)
    eccentricities[node] = max(dist.values())

# Determine radius, diameter, and centers
radius = min(eccentricities.values())
diameter = max(eccentricities.values())
centers = [node for node, ecc in eccentricities.items() if ecc == radius]


print(f"Radius of the MST: {radius}")
print(f"Diameter of the MST: {diameter}")
print(f"Center vertex/vertices: {centers}")
