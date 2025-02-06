class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)  

    def update(self, index, value):
        """Add 'value' at index 'index' (1-based)."""
        while index <= self.size:
            self.tree[index] += value
            index += index & -index  

    def query(self, index):
        """Get prefix sum up to index."""
        sum_ = 0
        while index > 0:
            sum_ += self.tree[index]
            index -= index & -index  
        return sum_

    def range_query(self, left, right):
        """Get sum of values in range [left, right]."""
        return self.query(right) - self.query(left - 1)

size = 10
fenwick = FenwickTree(size)
updates = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2]
for i, val in enumerate(updates, start=1):
    fenwick.update(i, val)

print("Prefix sum up to index 5:", fenwick.query(5))
print("Range sum from index 3 to 7:", fenwick.range_query(3, 7))
