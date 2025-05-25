import networkx as nx
import matplotlib.pyplot as plt

def input_graph():
    """Функция для ручного ввода графа"""
    print("\nВведите граф в формате:")
    print("1. Каждая строка описывает рёбра из вершины (формат: 'a b c' - рёбра из a в b и c)")
    print("2. Для завершения ввода введите пустую строку")
    print("3. Пример ввода:\n1 2 3\n2 3\n3 1 4\n4\n")

    G = nx.Graph()
    while True:
        line = input().strip()
        if not line:
            break
        parts = line.split()
        u = parts[0]
        for v in parts[1:]:
            G.add_edge(u, v)
    return G

def analyze_graph(G):
    """Анализ графа и вывод характеристик"""
    # 1. Независимые множества
    max_independent = nx.algorithms.approximation.maximum_independent_set(G)
    alpha = len(max_independent)

    # 2. Доминирующие множества
    min_dominating = nx.algorithms.dominating.dominating_set(G)
    gamma = len(min_dominating)

    # 3. Плотность графа
    density = nx.density(G)

    # 4. Дополнительные характеристики
    vertex_conn = nx.node_connectivity(G) if len(G) > 1 else 0
    edge_conn = nx.edge_connectivity(G) if len(G) > 1 else 0

    # Вывод результатов
    print("\nРезультаты анализа:")
    print(f"1. Максимальное независимое множество: {max_independent}")
    print(f"   Число независимости α(G): {alpha}")
    print(f"\n2. Минимальное доминирующее множество: {min_dominating}")
    print(f"   Число доминирования γ(G): {gamma}")
    print(f"\n3. Плотность графа: {density:.4f}")
    print(f"\n4. Дополнительные характеристики:")
    print(f"   Вершинная связность χ(G): {vertex_conn}")
    print(f"   Рёберная связность λ(G): {edge_conn}")

    # Визуализация
    nx.draw(G, with_labels=True, node_color='lightblue',
            node_size=800, edge_color='gray')
    plt.title("Визуализация графа")
    plt.show()

if __name__ == "__main__":
    print("Анализатор графов")
    print("-----------------")
    print("Вычисляет:")
    print("1. Независимые множества")
    print("2. Доминирующие множества")
    print("3. Плотность графа")
    print("4. Вершинную и рёберную связность\n")

    G = input_graph()
    if len(G.nodes()) == 0:
        print("Граф не содержит вершин!")
    else:
        analyze_graph(G)
