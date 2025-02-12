def heapify_up(heap, index):
    while index > 0:
        parent = (index - 1) // 2
        if heap[index] < heap[parent]:
            heap[index], heap[parent] = heap[parent], heap[index]
            index = parent
        else:
            break

def heapify_down(heap, index):
    n = len(heap)
    while True:
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < n and heap[left] < heap[smallest]:
            smallest = left
        if right < n and heap[right] < heap[smallest]:
            smallest = right

        if smallest != index:
            heap[index], heap[smallest] = heap[smallest], heap[index]
            index = smallest
        else:
            break

def insert(heap, value):
    heap.append(value)
    heapify_up(heap, len(heap) - 1)

def delete_element(heap, value):
    if value not in heap:
        print(f"Value {value} not found in the heap.")
        return

    index = heap.index(value)
    last = heap.pop()
    
    if index >= len(heap):
        return
    
    heap[index] = last
    parent = (index - 1) // 2
    
    if index > 0 and heap[index] < heap[parent]:
        heapify_up(heap, index)
    else:
        heapify_down(heap, index)

def main():
    heap = []
    while True:
        print("\n1. Insert")
        print("2. Delete")
        print("3. Search")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            value = int(input("Enter value to insert: "))
            insert(heap, value)
            print(f"Heap after insertion: {heap}")
        elif choice == '2':
            value = int(input("Enter value to delete: "))
            delete_element(heap, value)
            print(f"Heap after deletion: {heap}")
        elif choice == '3':
            value = int(input("Enter value to search: "))
            if value in heap:
                print(f"Value {value} found in the heap.")
            else:
                print(f"Value {value} not found in the heap.")
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
