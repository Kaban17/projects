import networkx as nx
import matplotlib.pyplot as plt

def input_adj_list():
    """Функция для ввода списка смежности графа"""
    adj_list = {}
    print("\nВведите список смежности (формат: 'вершина: сосед1, сосед2, ...')")
    print("Для завершения ввода оставьте строку пустой")
    while True:
        line = input().strip()
        if not line:
            break
        if ':' not in line:
            print("Ошибка: используйте формат 'вершина: сосед1, сосед2, ...'")
            continue

        node, neighbors = line.split(':', 1)
        node = node.strip()
        neighbors = [n.strip() for n in neighbors.split(',') if n.strip()]

        # Пробуем преобразовать в числа, если возможно
        try:
            node = int(node)
            neighbors = [int(n) for n in neighbors]
        except ValueError:
            pass

        adj_list[node] = neighbors
    return adj_list

def create_graph(adj_list, directed):
    """Создает граф из списка смежности"""
    G = nx.DiGraph() if directed else nx.Graph()
    for node in adj_list:
        for neighbor in adj_list[node]:
            G.add_edge(node, neighbor)
    return G

def analyze_graph(G, directed):
    """Анализирует граф и выводит результаты"""
    # Проверка связности
    if directed:
        is_connected = nx.is_weakly_connected(G)
    else:
        is_connected = nx.is_connected(G)

    if not is_connected:
        print("\nГраф не связный!")
        return

    # Вычисляем связности
    vertex_conn = nx.node_connectivity(G)
    edge_conn = nx.edge_connectivity(G)

    print(f"\nВершинная связность χ(G) = {vertex_conn}")
    print(f"Рёберная связность λ(G) = {edge_conn}")

    # Ввод вершин для разделяющего множества
    nodes = list(G.nodes())
    print("\nДоступные вершины:", nodes)
    while True:
        try:
            u = input("Введите первую вершину: ").strip()
            v = input("Введите вторую вершину: ").strip()

            # Пробуем преобразовать в число, если возможно
            try:
                u = int(u)
                v = int(v)
            except ValueError:
                pass

            if u not in nodes or v not in nodes:
                print("Ошибка: такой вершины нет в графе")
                continue

            if u == v:
                print("Ошибка: вершины должны быть разными")
                continue

            break
        except KeyboardInterrupt:
            exit()

    # Находим разделяющие множества
    try:
        vertex_cut = nx.minimum_node_cut(G, u, v)
        edge_cut = nx.minimum_edge_cut(G, u, v)

        print(f"\nМинимальное вершинное разделяющее множество между {u} и {v}: {vertex_cut}")
        print(f"Минимальное рёберное разделяющее множество между {u} и {v}: {edge_cut}")
    except nx.NetworkXError as e:
        print(f"\nОшибка: {e}")

def draw_graph(G, directed):
    """Визуализирует граф"""
    pos = nx.spring_layout(G)
    nx.draw(G, pos,
            with_labels=True,
            node_color='lightblue',
            node_size=800,
            edge_color='gray',
            arrows=directed,
            arrowstyle='-|>',
            arrowsize=20)
    plt.title("Визуализация графа")
    plt.show()

if __name__ == "__main__":
    print("Анализатор связности графа")
    print("--------------------------")

    # Ввод графа
    adj_list = input_adj_list()
    directed = input("Граф направленный? (y/n): ").lower().strip() == 'y'
    G = create_graph(adj_list, directed)

    # Анализ
    analyze_graph(G, directed)

    # Визуализация
    draw_graph(G, directed)
