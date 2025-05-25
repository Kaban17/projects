import networkx as nx
import matplotlib.pyplot as plt

def input_adj_list():
    """Запрашивает список смежности у пользователя."""
    adj_list = {}
    print("Введите список смежности (для завершения введите пустую строку):")
    print("Формат ввода: узел: сосед1, сосед2, ...")
    while True:
        line = input().strip()
        if not line:
            break
        if ':' not in line:
            print("Ошибка: отсутствует двоеточие. Используйте формат 'узел: сосед1, сосед2, ...'")
            continue
        node_part, neighbors_part = line.split(':', 1)
        node = node_part.strip()
        neighbors = [n.strip() for n in neighbors_part.split(',')]

        # Преобразование в числа, если возможно
        try:
            node = int(node)
        except ValueError:
            pass
        neighbors_list = []
        for n in neighbors:
            try:
                neighbors_list.append(int(n))
            except ValueError:
                neighbors_list.append(n)
        adj_list[node] = neighbors_list
    return adj_list

def create_graph(adj_list, directed):
    """Создаёт граф из списка смежности."""
    G = nx.DiGraph() if directed else nx.Graph()
    for node in adj_list:
        for neighbor in adj_list[node]:
            G.add_edge(node, neighbor)
    return G

def draw_graph(G, directed):
    """Рисует граф."""
    pos = nx.spring_layout(G)
    nx.draw(
        G, pos,
        with_labels=True,
        arrows=directed,
        node_color='lightblue',
        node_size=800,
        edge_color='gray',
        font_weight='bold'
    )
    plt.show()

def analyze_graph(G, directed):
    """Анализирует граф и выводит результаты."""
    # Транзитивное замыкание (только для направленных графов)
    if directed:
        G_trans = nx.transitive_closure(G)
        print("\nТранзитивное замыкание графа:")
        trans_adj_list = {}
        for node in G_trans.nodes():
            trans_adj_list[node] = list(G_trans.successors(node))
        for node in sorted(trans_adj_list):
            neighbors = ', '.join(map(str, sorted(trans_adj_list[node])))
            print(f"{node}: {neighbors}")
    else:
        print("\nТранзитивное замыкание не вычисляется для ненаправленных графов.")

    # Сильные компоненты связности (только для направленных графов)
    if directed:
        scc = list(nx.strongly_connected_components(G))
        print("\nСильные компоненты связности:")
        for i, component in enumerate(scc, 1):
            print(f"Компонента {i}: {', '.join(map(str, sorted(component)))}")
        is_strongly_connected = len(scc) == 1
        print(f"\nГраф {'сильно связный' if is_strongly_connected else 'не сильно связный'}.")
    else:
        print("\nСильные компоненты связности определены только для направленных графов.")

    # Односторонняя связность (только для направленных графов)
    if directed:
        is_unilaterally_connected = True
        nodes = list(G.nodes())
        for u in nodes:
            for v in nodes:
                if u != v and not nx.has_path(G, u, v) and not nx.has_path(G, v, u):
                    is_unilaterally_connected = False
                    break
            if not is_unilaterally_connected:
                break
        print(f"Граф {'односторонне связный' if is_unilaterally_connected else 'не односторонне связный'}.")
    else:
        print("Односторонняя связность определена только для направленных графов.")

    # Слабая связность
    if directed:
        undirected_G = G.to_undirected()
        is_weakly_connected = nx.is_connected(undirected_G)
    else:
        is_weakly_connected = nx.is_connected(G)
    print(f"Граф {'слабо связный' if is_weakly_connected else 'не слабо связный'}.")

if __name__ == "__main__":
    adj_list = input_adj_list()
    directed = input("Граф направленный? (y/n): ").lower().strip() == 'y'
    G = create_graph(adj_list, directed)
    analyze_graph(G, directed)
    draw_graph(G, directed)
