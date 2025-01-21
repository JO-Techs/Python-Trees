class BTreeNode:
    def __init__(self, t, is_leaf):
        self.t = t  
        self.is_leaf = is_leaf  
        self.keys = [] 
        self.children = []  

    def insert_non_full(self, key):
        i = len(self.keys) - 1

        if self.is_leaf:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            self.keys.insert(i + 1, key)
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1

            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1

            self.children[i].insert_non_full(key)

    def split_child(self, i):
        t = self.t
        child = self.children[i]
        new_child = BTreeNode(t, child.is_leaf)

        self.keys.insert(i, child.keys[t - 1])
        self.children.insert(i + 1, new_child)

        new_child.keys = child.keys[t:]
        child.keys = child.keys[:t - 1]

        if not child.is_leaf:
            new_child.children = child.children[t:]
            child.children = child.children[:t]

    def traverse(self):
        for i in range(len(self.keys)):
            if not self.is_leaf:
                self.children[i].traverse()
            print(self.keys[i], end=" ")

        if not self.is_leaf:
            self.children[-1].traverse()

    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1

        if i < len(self.keys) and self.keys[i] == key:
            return self

        if self.is_leaf:
            return None

        return self.children[i].search(key)

    def remove(self, key):
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1

        if idx < len(self.keys) and self.keys[idx] == key:
            if self.is_leaf:
                self.keys.pop(idx)
            else:
                self.remove_internal_node(idx)
        elif not self.is_leaf:
            flag = idx == len(self.keys)
            if len(self.children[idx].keys) < self.t:
                self.fill(idx)
            if flag and idx > len(self.keys):
                self.children[idx - 1].remove(key)
            else:
                self.children[idx].remove(key)
        else:
            print(f"Key {key} is not in the tree.")

    def remove_internal_node(self, idx):
        key = self.keys[idx]

        if len(self.children[idx].keys) >= self.t:
            pred = self.get_predecessor(idx)
            self.keys[idx] = pred
            self.children[idx].remove(pred)
        elif len(self.children[idx + 1].keys) >= self.t:
            succ = self.get_successor(idx)
            self.keys[idx] = succ
            self.children[idx + 1].remove(succ)
        else:
            self.merge(idx)
            self.children[idx].remove(key)

    def get_predecessor(self, idx):
        cur = self.children[idx]
        while not cur.is_leaf:
            cur = cur.children[-1]
        return cur.keys[-1]

    def get_successor(self, idx):
        cur = self.children[idx + 1]
        while not cur.is_leaf:
            cur = cur.children[0]
        return cur.keys[0]

    def fill(self, idx):
        if idx != 0 and len(self.children[idx - 1].keys) >= self.t:
            self.borrow_from_prev(idx)
        elif idx != len(self.keys) and len(self.children[idx + 1].keys) >= self.t:
            self.borrow_from_next(idx)
        else:
            if idx != len(self.keys):
                self.merge(idx)
            else:
                self.merge(idx - 1)

    def borrow_from_prev(self, idx):
        child = self.children[idx]
        sibling = self.children[idx - 1]

        child.keys.insert(0, self.keys[idx - 1])
        if not child.is_leaf:
            child.children.insert(0, sibling.children.pop())

        self.keys[idx - 1] = sibling.keys.pop()

    def borrow_from_next(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys[idx])
        if not child.is_leaf:
            child.children.append(sibling.children.pop(0))

        self.keys[idx] = sibling.keys.pop(0)

    def merge(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys.pop(idx))
        child.keys.extend(sibling.keys)

        if not child.is_leaf:
            child.children.extend(sibling.children)

        self.children.pop(idx + 1)


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def insert(self, key):
        root = self.root

        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, False)
            new_root.children.append(self.root)
            new_root.split_child(0)

            i = 0
            if new_root.keys[0] < key:
                i += 1

            new_root.children[i].insert_non_full(key)
            self.root = new_root
        else:
            root.insert_non_full(key)

    def traverse(self):
        if self.root:
            self.root.traverse()

    def search(self, key):
        if self.root:
            return self.root.search(key)
        return None

    def delete(self, key):
        if self.root:
            self.root.remove(key)
            if len(self.root.keys) == 0:
                if self.root.is_leaf:
                    self.root = None
                else:
                    self.root = self.root.children[0]


if __name__ == "__main__":
    t = 3  
    b_tree = BTree(t)

    while True:
        print("\nOptions:")
        print("1. Insert")
        print("2. Traverse")
        print("3. Search")
        print("4. Delete")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            key = int(input("Enter key to insert: "))
            b_tree.insert(key)
        elif choice == 2:
            print("Traversal of the tree:")
            b_tree.traverse()
            print()
        elif choice == 3:
            key = int(input("Enter key to search: "))
            result = b_tree.search(key)
            if result:
                print(f"Key {key} found in the tree.")
            else:
                print(f"Key {key} not found in the tree.")
        elif choice == 4:
            key = int(input("Enter key to delete: "))
            b_tree.delete(key)
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")
