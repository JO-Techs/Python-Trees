class PatriciaNode:
    def __init__(self, key='', value=None):
        self.key = key  
        self.value = value 
        self.children = {}  

class PatriciaTree:
    def __init__(self):
        self.root = PatriciaNode()

    def insert(self, key, value):
        node = self.root
        while True:
            for edge, child in node.children.items():
                common_prefix = self._common_prefix(key, edge)
                if common_prefix:
                    if common_prefix == edge:  
                        key = key[len(edge):]  
                        node = child
                        break
                    else:
                        new_node = PatriciaNode(key=edge[len(common_prefix):])
                        new_node.children = child.children
                        new_node.value = child.value
                        node.children[common_prefix] = PatriciaNode()
                        node.children[common_prefix].children = {new_node.key: new_node}
                        if key[len(common_prefix):]:
                            node.children[common_prefix].children[key[len(common_prefix):]] = PatriciaNode(key=key[len(common_prefix):], value=value)
                        else:
                            node.children[common_prefix].value = value
                        return
            else:
                node.children[key] = PatriciaNode(key=key, value=value)
                return

    def search(self, key):
        node = self.root
        while key:
            for edge, child in node.children.items():
                if key.startswith(edge):  
                    key = key[len(edge):] 
                    node = child
                    break
            else:
                return None
        return node.value
    def traverse(self, node=None, prefix=""):
        if node is None:
            node = self.root
        if node.value is not None:
            print(f"{prefix} -> {node.value}")
        for edge, child in node.children.items():
            self.traverse(child, prefix + edge)
    def delete(self, key):
        def _delete(node, key, parent=None, edge=None):
            if not key:
                if node.value is None:
                    return False  # Key does not exist
                node.value = None  # Mark the key as deleted
                if not node.children:  # Remove the node if it's a leaf
                    if parent and edge:
                        del parent.children[edge]
                return True
            for child_edge, child in node.children.items():
                if key.startswith(child_edge):
                    success = _delete(child, key[len(child_edge):], node, child_edge)
                    # Clean up empty nodes
                    if success and not child.children and child.value is None:
                        del node.children[child_edge]
                    return success
            return False  # Key not found
        return _delete(self.root, key)
    def _common_prefix(self, key1, key2):
        i = 0
        while i < len(key1) and i < len(key2) and key1[i] == key2[i]:
            i += 1
        return key1[:i]
def main():
    print("PATRICIA Tree - Example")
    tree = PatriciaTree()
    while True:
        print("\nMenu:")
        print("1. Insert")
        print("2. Search")
        print("3. Traverse")
        print("4. Delete")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            key = input("Enter the key to insert: ")
            value = input("Enter the value to associate with the key: ")
            tree.insert(key, value)
            print(f"Key '{key}' with value '{value}' inserted.")
        elif choice == "2":
            key = input("Enter the key to search: ")
            result = tree.search(key)
            if result is not None:
                print(f"Key '{key}' found with value: {result}")
            else:
                print(f"Key '{key}' not found.")
        elif choice == "3":
            print("\nPATRICIA Tree Traversal:")
            tree.traverse()
        elif choice == "4":
            key = input("Enter the key to delete: ")
            if tree.delete(key):
                print(f"Key '{key}' deleted successfully.")
            else:
                print(f"Key '{key}' not found.")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
