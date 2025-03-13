class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def build_perfect_tree():
    height = int(input("Enter the height of the perfect binary tree: "))
    node_count = 2 ** (height + 1) - 1
    print(f"Enter {node_count} values for the tree (level order):")
    
    values = []
    while len(values) < node_count:
        try:
            val = int(input(f"Value {len(values)+1}: "))
            values.append(val)
        except ValueError:
            print("Please enter a valid integer!")
    
    nodes = [Node(val) for val in values]
    for i in range(node_count):
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        if left_idx < node_count:
            nodes[i].left = nodes[left_idx]
        if right_idx < node_count:
            nodes[i].right = nodes[right_idx]
    
    return nodes[0] if nodes else None

def print_traversals(root):
    print("\nTraversals:")
    print("Pre-order:  ", end="")
    pre_order(root)
    
    print("\nIn-order:   ", end="")
    in_order(root)
    
    print("\nPost-order: ", end="")
    post_order(root)
    
    print("\nLevel-order:", end="")
    level_order(root)
    print()

def pre_order(node):
    if node:
        print(node.value, end=" ")
        pre_order(node.left)
        pre_order(node.right)

def in_order(node):
    if node:
        in_order(node.left)
        print(node.value, end=" ")
        in_order(node.right)

def post_order(node):
    if node:
        post_order(node.left)
        post_order(node.right)
        print(node.value, end=" ")

def level_order(root):
    if not root:
        return
    queue = [root]
    while queue:
        node = queue.pop(0)
        print(node.value, end=" ")
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

if __name__ == "__main__":
    root = build_perfect_tree()
    print_traversals(root)
