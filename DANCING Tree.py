class DancingTreeNode:
    def __init__(self, t):
        self.t = t  # Minimum degree
        self.keys = []  # Keys in the node
        self.children = []  # Child pointers
        self.leaf = True  # Is this a leaf node?

    def is_full(self):
        return len(self.keys) == 2 * self.t - 1

    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.leaf:
            # Insert the key into the correct position
            self.keys.append(None)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            # Find the child to insert the key into
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if self.children[i].is_full():
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i):
        t = self.t
        child = self.children[i]
        new_child = DancingTreeNode(t)
        new_child.leaf = child.leaf
        self.children.insert(i + 1, new_child)
        self.keys.insert(i, child.keys[t - 1])
        new_child.keys = child.keys[t:]
        child.keys = child.keys[:t - 1]
        if not child.leaf:
            new_child.children = child.children[t:]
            child.children = child.children[:t]


class DancingTree:
    def __init__(self, t):
        self.t = t  # Minimum degree
        self.root = DancingTreeNode(t)

    def insert(self, key):
        root = self.root
        if root.is_full():
            new_root = DancingTreeNode(self.t)
            self.root = new_root
            new_root.leaf = False
            new_root.children.append(root)
            new_root.split_child(0)
            new_root.insert_non_full(key)
        else:
            root.insert_non_full(key)

    def traverse(self, node=None):
        if node is None:
            node = self.root
        for i, key in enumerate(node.keys):
            if not node.leaf:
                self.traverse(node.children[i])
            print(key, end=" ")
        if not node.leaf:
            self.traverse(node.children[-1])

    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return True
        if node.leaf:
            return False
        return self.search(key, node.children[i])

    def delete(self, key):
        # Deletion in a Dancing Tree involves handling cases of underflow and merging.
        # For simplicity, deletion here just marks the node as unbalanced.
        print(f"Deletion of {key} is not fully implemented in this simplified Dancing Tree.")
        return False


def main():
    print("Dancing Tree Implementation")
    t = int(input("Enter the minimum degree of the tree (t): "))
    tree = DancingTree(t)

    while True:
        print("\nMenu:")
        print("1. Insert")
        print("2. Traverse")
        print("3. Search")
        print("4. Delete")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            key = int(input("Enter the value to insert: "))
            tree.insert(key)
        elif choice == "2":
            print("Tree traversal: ", end="")
            tree.traverse()
            print()
        elif choice == "3":
            key = int(input("Enter the value to search: "))
            found = tree.search(key)
            print(f"Key {key} {'found' if found else 'not found'} in the tree.")
        elif choice == "4":
            key = int(input("Enter the value to delete: "))
            tree.delete(key)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
