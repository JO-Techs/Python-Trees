class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

class TernaryTree:
    def __init__(self):
        self.root = None
        self.n = 3

    def insert(self, value, parent_value=None):
        new_node = Node(value)
        if not self.root:
            self.root = new_node
            return True
        if parent_value is None:
            return False
        parent_node = self.search(self.root, parent_value)
        if parent_node and len(parent_node.children) < self.n:
            parent_node.children.append(new_node)
            return True
        return False

    def search(self, node, value):
        if not node:
            return None
        if node.value == value:
            return node
        for child in node.children:
            result = self.search(child, value)
            if result:
                return result
        return None

    def delete(self, value):
        if not self.root:
            return False
        if self.root.value == value:
            self.root = None
            return True
        return self._delete_helper(self.root, value)

    def _delete_helper(self, node, value):
        for i, child in enumerate(node.children):
            if child.value == value:
                node.children.pop(i)
                return True
            if self._delete_helper(child, value):
                return True
        return False

    def traverse(self, node, result):
        if not node:
            return
        result.append(node.value)
        for child in node.children:
            self.traverse(child, result)

    def get_traversal(self):
        result = []
        self.traverse(self.root, result)
        return result

def main():
    tree = TernaryTree()

    while True:
        print("\n1. Insert")
        print("2. Delete")
        print("3. Search")
        print("4. Traverse")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            value = int(input("Enter the value to insert: "))
            parent_value = input("Enter the parent value (leave blank if root): ")
            parent_value = int(parent_value) if parent_value else None
            if tree.insert(value, parent_value):
                print("Inserted successfully.")
            else:
                print("Insertion failed.")
        elif choice == 2:
            value = int(input("Enter the value to delete: "))
            if tree.delete(value):
                print("Deleted successfully.")
            else:
                print("Deletion failed.")
        elif choice == 3:
            value = int(input("Enter the value to search: "))
            node = tree.search(tree.root, value)
            if node:
                print("Value found.")
            else:
                print("Value not found.")
        elif choice == 4:
            traversal = tree.get_traversal()
            print("Traversal:", traversal)
        elif choice == 5:
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
