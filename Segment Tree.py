class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr[:]
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self.build(0, 0, self.n - 1)

    def build(self, node, start, end):
        if start == end:
            self.tree[node] = self.arr[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node + 1, start, mid)
            self.build(2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self.query(2 * node + 1, start, mid, l, r) + \
               self.query(2 * node + 2, mid + 1, end, l, r)

    def range_sum(self, l, r):
        if self.n == 0 or l < 0 or r >= self.n or l > r:
            return "Invalid range"
        return self.query(0, 0, self.n - 1, l, r)

def main():
    arr = []
    segment_tree = None
    
    while True:
        print("\nMenu:")
        print("1. Insert")
        print("2. Delete")
        print("3. Traverse")
        print("4. Range Sum Query")
        print("5. Exit")
        choice = int(input("Enter choice: "))

        if choice == 1:
            value = int(input("Enter value to insert: "))
            arr.append(value)
            segment_tree = SegmentTree(arr)
        elif choice == 2:
            if not arr:
                print("Array is empty!")
                continue
            index = int(input(f"Enter index to delete (0-{len(arr) - 1}): "))
            if index < 0 or index >= len(arr):
                print("Invalid index!")
                continue
            arr.pop(index)
            segment_tree = SegmentTree(arr)
        elif choice == 3:
            print("Array elements:", arr)
        elif choice == 4:
            if not arr:
                print("Array is empty!")
                continue
            l, r = map(int, input(f"Enter range (0-{len(arr) - 1}): ").split())
            print(f"Sum from {l} to {r}: {segment_tree.range_sum(l, r)}")
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
