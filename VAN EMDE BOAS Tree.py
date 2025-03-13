class VEBTree:
    def __init__(self, u):
        self.u = u  # Universe size (must be a power of two)
        self.min_val = None
        self.max_val = None

        if u < 2:
            raise ValueError("Universe size must be at least 2")
        if (u & (u - 1)) != 0:
            raise ValueError("Universe size must be a power of two")

        self.summary = None
        self.clusters = None

        if u > 2:
            exponent = u.bit_length() - 1
            self.upper_sqrt = 1 << ((exponent + 1) // 2)
            self.lower_sqrt = 1 << (exponent // 2)
            self.summary = VEBTree(self.upper_sqrt)
            self.clusters = [VEBTree(self.lower_sqrt) for _ in range(self.upper_sqrt)]

    def member(self, x):
        if x < 0 or x >= self.u:
            return False
        if x == self.min_val or x == self.max_val:
            return True
        if self.u == 2:
            return False
        cluster_idx = x // self.lower_sqrt
        idx_in_cluster = x % self.lower_sqrt
        return self.clusters[cluster_idx].member(idx_in_cluster)

    def insert(self, x):
        if x < 0 or x >= self.u:
            raise ValueError("Value out of range")
        if self.min_val is None:
            self.min_val = self.max_val = x
            return
        if x < self.min_val:
            x, self.min_val = self.min_val, x
        if self.u > 2:
            cluster_idx = x // self.lower_sqrt
            idx_in_cluster = x % self.lower_sqrt
            if self.clusters[cluster_idx].min_val is None:
                self.summary.insert(cluster_idx)
            self.clusters[cluster_idx].insert(idx_in_cluster)
        if x > self.max_val:
            self.max_val = x

    def successor(self, x):
        if x < 0 or x >= self.u:
            return None
        if self.u == 2:
            if x == 0 and self.max_val == 1:
                return 1
            else:
                return None
        if self.min_val is not None and x < self.min_val:
            return self.min_val
        cluster_idx = x // self.lower_sqrt
        idx_in_cluster = x % self.lower_sqrt
        max_in_cluster = self.clusters[cluster_idx].max_val
        if max_in_cluster is not None and idx_in_cluster < max_in_cluster:
            offset = self.clusters[cluster_idx].successor(idx_in_cluster)
            if offset is not None:
                return cluster_idx * self.lower_sqrt + offset
        else:
            next_cluster = self.summary.successor(cluster_idx)
            if next_cluster is not None:
                offset = self.clusters[next_cluster].min_val
                return next_cluster * self.lower_sqrt + offset
            else:
                if self.max_val is not None and x < self.max_val:
                    return self.max_val
        return None

    def delete(self, x):
        if x < 0 or x >= self.u:
            raise ValueError("Value out of range")
        if self.min_val == self.max_val:
            if x == self.min_val:
                self.min_val = self.max_val = None
            return
        if self.u == 2:
            if x == self.min_val:
                self.min_val = self.max_val
            else:
                self.max_val = self.min_val
            return
        if x == self.min_val:
            first_cluster = self.summary.min_val
            idx = self.clusters[first_cluster].min_val
            self.min_val = first_cluster * self.lower_sqrt + idx
            self.clusters[first_cluster].delete(idx)
            if self.clusters[first_cluster].min_val is None:
                self.summary.delete(first_cluster)
        else:
            cluster_idx = x // self.lower_sqrt
            idx = x % self.lower_sqrt
            self.clusters[cluster_idx].delete(idx)
            if self.clusters[cluster_idx].min_val is None:
                self.summary.delete(cluster_idx)
        # Update max_val
        if self.summary.max_val is None:
            self.max_val = self.min_val
        else:
            last_cluster = self.summary.max_val
            self.max_val = last_cluster * self.lower_sqrt + self.clusters[last_cluster].max_val

    def get_min(self):
        return self.min_val

    def get_max(self):
        return self.max_val

# Example usage
if __name__ == "__main__":
    veb = VEBTree(16)
    veb.insert(2)
    veb.insert(3)
    veb.insert(7)
    veb.insert(14)
    
    print("Member 3:", veb.member(3))  # True
    print("Member 4:", veb.member(4))  # False
    
    print("Successor of 3:", veb.successor(3))  # 7
    print("Min:", veb.get_min())  # 2
    print("Max:", veb.get_max())  # 14
    
    veb.delete(3)
    print("Member 3 after delete:", veb.member(3))  # False
    print("Successor of 2:", veb.successor(2))  # 7
