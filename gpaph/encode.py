
def prufer_decode(code):
    n = len(code) + 2  # число вершин
    p = code[:]        # копия кода, чтобы не изменять оригинал
    s = list(range(1, n + 1))  # список всех вершин

    edges = []

    while p:
        # Найти минимальную вершину i_j из s, которая не встречается в p
        leaf = min(v for v in s if v not in p)

        # Добавить ребро (leaf, p[0])
        edges.append((leaf, p[0]))

        # Удаляем leaf из s и p[0] из p (одно вхождение)
        s.remove(leaf)
        p.pop(0)

    # В конце в s остаются ровно две вершины — соединяем их
    edges.append((s[0], s[1]))

    return edges


# Пример использования
code = [4, 2, 2, 6, 7, 5, 2, 10, 7, 3][::-1]
tree_edges = prufer_decode(code)

print("Рёбра восстановленного дерева:")
for u, v in tree_edges:
    print(f"({u}, {v})")

def normalize_edges(edges):
    # В каждом ребре сортируем вершины, потом сортируем список рёбер
    normalized = [tuple(sorted(edge)) for edge in edges]
    return sorted(normalized)

expected_edges = [
    (5, 11), (1, 4),  (2, 5), (6, 9),
    (2, 4), (2, 10), (3, 12), (6, 7),
    (7, 10), (3, 7), (2, 8)
]
# Предположим, tree_edges — рёбра, полученные из кода Прюфера
