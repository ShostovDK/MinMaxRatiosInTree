import random
import time

# Класс Node представляет узел дерева.
# Каждый узел имеет вес, список потомков и арность (максимальное количество потомков).
class Node:
    def __init__(self, weight, arity=None):
        self.weight = weight
        self.children = []
        self.arity = arity

    def add_child(self, child):
        self.children.append(child)

    # Метод sum_weights вычисляет сумму весов узла и всех его потомков.
    def sum_weights(self):
        if not self.children:
            return self.weight
        else:
            return self.weight + sum([child.sum_weights() for child in self.children])

    # Метод count_nodes вычисляет количество узлов узла и всех его потомков.
    def count_nodes(self):
        if not self.children:
            return 1
        else:
            return 1 + sum([child.count_nodes() for child in self.children])

    # Метод ratio вычисляет отношение суммы весов к количеству узлов.
    def ratio(self):
        return self.sum_weights() / self.count_nodes()

    # Метод find_subtrees_with_extreme_ratios находит поддеревья с минимальным и максимальным отношением.
    def find_subtrees_with_extreme_ratios(self):
        if not self.children:
            return (self, self)

        min_subtree = self.children[0]
        max_subtree = self.children[0]

        for child in self.children:
            child_min_subtree, child_max_subtree = child.find_subtrees_with_extreme_ratios()

            if child_min_subtree.ratio() < min_subtree.ratio():
                min_subtree = child_min_subtree

            if child_max_subtree.ratio() > max_subtree.ratio():
                max_subtree = child_max_subtree

        return (min_subtree, max_subtree)

    # Метод get_all_nodes возвращает список всех узлов дерева.
    def get_all_nodes(self):
        if not self.children:
            return [self]
        else:
            nodes = [self]
            for child in self.children:
                nodes.extend(child.get_all_nodes())
            return nodes

# Функция generate_n_ary_tree генерирует N-дерево с заданным количеством узлов и арностью.
def generate_n_ary_tree(n_nodes, arity, weight_range=(1, 10)):
    if n_nodes <= 0:
        return None

    root = Node(random.randint(*weight_range), arity if arity is not None else None)
    n_remaining_nodes = n_nodes - 1

    while n_remaining_nodes > 0:
        parent = random.choice(list(filter(lambda node: len(node.children) < (node.arity if node.arity is not None else n_remaining_nodes), [root] + root.get_all_nodes())))
        child = Node(random.randint(*weight_range), arity if arity is not None else None)
        parent.add_child(child)
        n_remaining_nodes -= 1

    return root

# Функция print_tree выводит дерево на экран.
def print_tree(node, level=0, is_last=True, print_subtree=False):
    child_count = len(node.children)
    if child_count != 0:
        is_last = False

    prefix = '  ' * level
    if is_last:
        suffix = '   '
        line_type = '└── '
    else:
        suffix = '│  '
        line_type = '├── '

    if print_subtree:
        subtree_str = f" (поддерево: {node.sum_weights()} весов, {node.count_nodes()} узлов, отношение: {node.ratio():.2f})"
    else:
        subtree_str = ""

    print(f"{prefix}{line_type}{node.weight} (отношение: {node.ratio():.2f}){subtree_str}{suffix}")

    for i, child in enumerate(node.children):
        print_tree(child, level + 1, i == child_count - 1, print_subtree)

# Функция create_tree_manually позволяет создавать дерево вручную.
def create_tree_manually():
    print("Создание дерева вручную.")
    print("Введите 'x' для завершения ввода.")

    root = Node(int(input("Введите вес корня: ")))
    children = []

    while True:
        child_weight = input("Введите вес ребенка (или 'x' для завершения): ")
        if child_weight.lower() == 'x':
            break

        try:
            child_weight = int(child_weight)
        except ValueError:
            print("Неверный ввод. Попробуйте снова.")
            continue

        child = Node(child_weight)
        children.append(child)

        while True:
            add_child = input(f"Добавить ребенка для узла {child.weight}? (y/n): ").lower()
            if add_child == 'y':
                new_child_weight = int(input(f"Введите вес нового ребенка для узла {child.weight}: "))
                new_child = Node(new_child_weight)
                child.add_child(new_child)
                continue
            elif add_child == 'n':
                break
            else:
                print("Неверный ввод. Попробуйте снова.")

    root.children = children
    return root

# Главная функция.
def main():
    while True:
        try:
            n_nodes = int(input("Введите количество узлов: "))
            if n_nodes < 1:
                raise ValueError("Количество узлов должно быть положительным числом.")
            break
        except ValueError as e:
            print(e)

    while True:
        try:
            arity_input = int(input("Введите арность (или -1 для случайной арности): "))
            if arity_input < -1:
                raise ValueError("Арность должна быть -1 или положительным числом.")
            break
        except ValueError as e:
            print(e)

    arity = arity_input if arity_input != -1 else None

    while True:
        creation_method = input("Выберите способ создания дерева (генерация - 'g', вручную - 'm'): ").lower()
        if creation_method == 'g':
            start_time = time.time()
            tree = generate_n_ary_tree(n_nodes, arity)
            end_time = time.time()

            print(f"Время генерации дерева: {end_time - start_time:.4f} секунд")
            print("Дерево:")
            print_tree(tree)

            start_time = time.time()
            min_subtree, max_subtree = tree.find_subtrees_with_extreme_ratios()
            end_time = time.time()

            print(f"\nВремя поиска поддеревьев с минимальным и максимальным отношением: {end_time - start_time:.4f} секунд")
            print(f"Поддерево с минимальным отношением:")
            print_tree(min_subtree, print_subtree=True)
            print(f"Сумма весов: {min_subtree.sum_weights()}")
            print(f"Количество узлов: {min_subtree.count_nodes()}")
            print(f"Отношение: {min_subtree.ratio():.2f}")

            print(f"\nПоддерево с максимальным отношением:")
            print_tree(max_subtree, print_subtree=True)
            print(f"Сумма весов: {max_subtree.sum_weights()}")
            print(f"Количество узлов: {max_subtree.count_nodes()}")
            print(f"Отношение: {max_subtree.ratio():.2f}")
            break
        elif creation_method == 'm':
            tree = create_tree_manually()

            print("Дерево:")
            print_tree(tree)

            start_time = time.time()
            min_subtree, max_subtree = tree.find_subtrees_with_extreme_ratios()
            end_time = time.time()

            print(f"\nВремя поиска поддеревьев с минимальным и максимальным отношением: {end_time - start_time:.4f} секунд")

            print(f"Поддерево с минимальным отношением:")
            print_tree(min_subtree, print_subtree=True)
            print(f"Сумма весов: {min_subtree.sum_weights()}")
            print(f"Количество узлов: {min_subtree.count_nodes()}")
            print(f"Отношение: {min_subtree.ratio():.2f}")

            print(f"\nПоддерево с максимальным отношением:")
            print_tree(max_subtree, print_subtree=True)
            print(f"Сумма весов: {max_subtree.sum_weights()}")
            print(f"Количество узлов: {max_subtree.count_nodes()}")
            print(f"Отношение: {max_subtree.ratio():.2f}")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
