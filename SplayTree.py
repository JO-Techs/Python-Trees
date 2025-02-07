class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        node = Node(key)
        if self.root is None:
            self.root = node
            return
        current = self.root
        parent = None
        while current is not None:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                self._splay(current)
                return
        node.parent = parent
        if key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self._splay(node)

    def search(self, key):
        node = self.root
        prev = None
        while node is not None:
            prev = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return True
        if prev is not None:
            self._splay(prev)
        return False

    def delete(self, key):
        if not self.search(key):
            return False
        if self.root.left is None:
            self.root = self.root.right
            if self.root is not None:
                self.root.parent = None
        elif self.root.right is None:
            self.root = self.root.left
            if self.root is not None:
                self.root.parent = None
        else:
            left_tree = self.root.left
            right_tree = self.root.right
            left_tree.parent = None
            right_tree.parent = None
            max_left = left_tree
            while max_left.right is not None:
                max_left = max_left.right
            self.root = left_tree
            self._splay(max_left)
            self.root.right = right_tree
            if right_tree is not None:
                right_tree.parent = self.root
        return True

    def _splay(self, node):
        while node.parent is not None:
            parent = node.parent
            grandparent = parent.parent
            if grandparent is None:
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            else:
                if parent == grandparent.left:
                    if node == parent.left:
                        self._right_rotate(grandparent)
                        self._right_rotate(parent)
                    else:
                        self._left_rotate(parent)
                        self._right_rotate(grandparent)
                else:
                    if node == parent.right:
                        self._left_rotate(grandparent)
                        self._left_rotate(parent)
                    else:
                        self._right_rotate(parent)
                        self._left_rotate(grandparent)

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right is not None:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def display(self):
        print("In-order traversal:", self._in_order_traversal(self.root))
        
    def _in_order_traversal(self, node):
        result = []
        if node:
            result = self._in_order_traversal(node.left)
            result.append(node.key)
            result += self._in_order_traversal(node.right)
        return result

def main():
    tree = SplayTree()
    while True:
        command = input("\nEnter command (insert, delete, search, display, exit): ").strip().lower()
        if command == 'exit':
            break
        elif command == 'insert':
            key = int(input("Enter key to insert: "))
            tree.insert(key)
            print(f"Inserted {key}")
        elif command == 'delete':
            key = int(input("Enter key to delete: "))
            if tree.delete(key):
                print(f"Deleted {key}")
            else:
                print(f"Key {key} not found")
        elif command == 'search':
            key = int(input("Enter key to search: "))
            if tree.search(key):
                print(f"Key {key} found")
            else:
                print(f"Key {key} not found")
        elif command == 'display':
            tree.display()
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
