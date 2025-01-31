#include <stdio.h>
#include <stdlib.h>

int *arr = NULL;
int arr_size = 0;
int *segment_tree = NULL;
int segment_tree_size = 0;

int calculate_tree_size(int n) {
    if (n == 0) return 0;
    int next_power = 1;
    while (next_power < n) {
        next_power <<= 1;
    }
    return 2 * next_power - 1;
}

void build(int node, int start, int end) {
    if (start == end) {
        segment_tree[node] = arr[start];
    } else {
        int mid = (start + end) / 2;
        build(2 * node + 1, start, mid);
        build(2 * node + 2, mid + 1, end);
        segment_tree[node] = segment_tree[2 * node + 1] + segment_tree[2 * node + 2];
    }
}

int query(int node, int start, int end, int l, int r) {
    if (r < start || end < l) return 0;
    if (l <= start && end <= r) return segment_tree[node];
    int mid = (start + end) / 2;
    return query(2 * node + 1, start, mid, l, r) + 
           query(2 * node + 2, mid + 1, end, l, r);
}

void free_memory() {
    free(arr);
    free(segment_tree);
    arr = NULL;
    segment_tree = NULL;
    arr_size = 0;
    segment_tree_size = 0;
}

int main() {
    int choice;
    do {
        printf("\nMenu:\n");
        printf("1. Insert\n");
        printf("2. Delete\n");
        printf("3. Traverse\n");
        printf("4. Range Sum Query\n");
        printf("5. Exit\n");
        printf("Enter choice: ");
        scanf("%d", &choice);

        switch(choice) {
            case 1: {
                int value;
                printf("Enter value to insert: ");
                scanf("%d", &value);
                int *temp = realloc(arr, (arr_size + 1) * sizeof(int));
                if (!temp) {
                    printf("Memory allocation failed!\n");
                    break;
                }
                arr = temp;
                arr[arr_size++] = value;
                
                free(segment_tree);
                segment_tree = NULL;
                if (arr_size > 0) {
                    segment_tree_size = calculate_tree_size(arr_size);
                    segment_tree = malloc(segment_tree_size * sizeof(int));
                    if (!segment_tree) {
                        printf("Segment tree allocation failed!\n");
                        free_memory();
                        exit(1);
                    }
                    build(0, 0, arr_size - 1);
                }
                break;
            }
            case 2: {
                if (arr_size == 0) {
                    printf("Array is empty!\n");
                    break;
                }
                int index;
                printf("Enter index to delete (0-%d): ", arr_size - 1);
                scanf("%d", &index);
                if (index < 0 || index >= arr_size) {
                    printf("Invalid index!\n");
                    break;
                }
                for (int i = index; i < arr_size - 1; i++)
                    arr[i] = arr[i + 1];
                arr_size--;
                arr = realloc(arr, arr_size * sizeof(int));
                
                free(segment_tree);
                segment_tree = NULL;
                if (arr_size > 0) {
                    segment_tree_size = calculate_tree_size(arr_size);
                    segment_tree = malloc(segment_tree_size * sizeof(int));
                    if (!segment_tree) {
                        printf("Segment tree allocation failed!\n");
                        free_memory();
                        exit(1);
                    }
                    build(0, 0, arr_size - 1);
                }
                break;
            }
            case 3: {
                printf("Array elements (%d): ", arr_size);
                for (int i = 0; i < arr_size; i++)
                    printf("%d ", arr[i]);
                printf("\n");
                break;
            }
            case 4: {
                if (arr_size == 0) {
                    printf("Array is empty!\n");
                    break;
                }
                int l, r;
                printf("Enter range (0-%d): ", arr_size - 1);
                scanf("%d %d", &l, &r);
                if (l < 0 || r >= arr_size || l > r) {
                    printf("Invalid range!\n");
                    break;
                }
                printf("Sum from %d to %d: %d\n", l, r, query(0, 0, arr_size - 1, l, r));
                break;
            }
            case 5:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice!\n");
        }
    } while (choice != 5);

    free_memory();
    return 0;
}