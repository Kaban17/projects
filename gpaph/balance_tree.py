class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

# Строим дерево T вручную
nodes = {i: Node(i) for i in range(1, 13)}

nodes[1].left = nodes[2]
nodes[2].left = nodes[5]
nodes[2].right = nodes[3]
nodes[3].left = nodes[6]
nodes[3].right = nodes[4]
nodes[4].left = nodes[7]
nodes[7].left = nodes[10]
nodes[10].left = nodes[12]
nodes[7].right = nodes[8]
nodes[8].left = nodes[11]
nodes[6].left = nodes[9]

root = nodes[1]

def is_balanced(root):
    def check(node):
        if not node:
            return 0, True
        lh, lb = check(node.left)
        rh, rb = check(node.right)
        height = max(lh, rh) + 1
        balanced = lb and rb and abs(lh - rh) <= 1
        return height, balanced
    height, balanced = check(root)
    return balanced, height

def deepest_path(node):
    if not node:
        return [], 0
    left_path, left_depth = deepest_path(node.left)
    right_path, right_depth = deepest_path(node.right)

    if left_depth > right_depth:
        return [node.val] + left_path, left_depth + 1
    else:
        return [node.val] + right_path, right_depth + 1

def build_balanced_tree_from_list(vals):
    """Строит сбалансированное дерево из отсортированного списка"""
    if not vals:
        return None
    mid = len(vals) // 2
    node = Node(vals[mid])
    node.left = build_balanced_tree_from_list(vals[:mid])
    node.right = build_balanced_tree_from_list(vals[mid+1:])
    return node

def largest_balanced_subtree(node):
    if not node:
        return 0, 0, None

    lh, ls, lsub = largest_balanced_subtree(node.left)
    rh, rs, rsub = largest_balanced_subtree(node.right)

    if abs(lh - rh) <= 1:
        return max(lh, rh) + 1, ls + rs + 1, node
    else:
        return (lh, ls, lsub) if ls >= rs else (rh, rs, rsub)

def print_tree(node, level=0, prefix="Root:"):
    if not node:
        print(" " * (level * 4) + prefix + " None")
        return
    print(" " * (level * 4) + prefix + f" {node.val}")
    print_tree(node.left, level + 1, prefix="L---")
    print_tree(node.right, level + 1, prefix="R---")

def count_nodes(node):
    if not node:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)

# --- Основной код ---
balanced, height = is_balanced(root)
print(f"Сбалансировано: {balanced}")
print(f"Высота дерева T: {height}")

path, depth = deepest_path(root)
print("Самый длинный путь от корня:", " -> ".join(map(str, path)))
print("Глубина (в рёбрах):", depth - 1)

# Строим сбалансированное дерево из того же количества узлов
node_count = count_nodes(root)
vals = list(range(1,  node_count))  # Значения узлов можно любые
new_tree = build_balanced_tree_from_list(vals)

print("\nПостроенное сбалансированное дерево с тем же числом узлов:")
print_tree(new_tree)

# Самое большое сбалансированное поддерево
_, size, subtree = largest_balanced_subtree(root)
print(f"\nРазмер наибольшего сбалансированного поддерева: {size}")
print("Структура наибольшего сбалансированного поддерева:")
print_tree(subtree)
