import random
import time

SIZE = 1000

def bubble_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(n-1):
        swapped = False
        for j in range(n-i-1):
            comparisons += 1
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return comparisons, swaps

def insertion_sort(arr):
    comparisons = 0
    swaps = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j+1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break
        arr[j+1] = key
        if j+1 != i:
            swaps += 1
    return comparisons, swaps

def merge_sort(arr):
    comparisons = [0]
    swaps = [0]
    
    def merge_sort_helper(arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]

            merge_sort_helper(L)
            merge_sort_helper(R)

            i = j = k = 0
            while i < len(L) and j < len(R):
                comparisons[0] += 1
                if L[i] < R[j]:
                    arr[k] = L[i]
                    swaps[0] += 1
                    i += 1
                else:
                    arr[k] = R[j]
                    swaps[0] += 1
                    j += 1
                k += 1

            while i < len(L):
                arr[k] = L[i]
                swaps[0] += 1
                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                swaps[0] += 1
                j += 1
                k += 1
    
    merge_sort_helper(arr)
    return comparisons[0], swaps[0]

def quick_sort(arr):
    comparisons = [0]
    swaps = [0]
    
    def quick_sort_helper(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr)//2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        comparisons[0] += len(arr) - 1
        swaps[0] += len(left) + len(right)
        return quick_sort_helper(left) + middle + quick_sort_helper(right)
    
    sorted_arr = quick_sort_helper(arr.copy())
    return comparisons[0], swaps[0]

def generate_random_list():
    return [random.randint(0, 9999) for _ in range(SIZE)]

def generate_sorted_list():
    return list(range(SIZE))

def generate_reverse_list():
    return list(range(SIZE-1, -1, -1))

def measure_time(sort_func, arr_generator, sort_name, array_type):
    arr = arr_generator()
    
    if sort_func.__name__ == 'quick_sort':
        start = time.perf_counter()
        comparisons, swaps = sort_func(arr.copy())
        end = time.perf_counter()
    else:
        arr_copy = arr.copy()
        start = time.perf_counter()
        comparisons, swaps = sort_func(arr_copy)
        end = time.perf_counter()
    
    elapsed = (end - start) * 1000
    print(f"{sort_name:>14} {array_type:>9}: {elapsed:>10.2f} ms | Comparaciones: {comparisons:>8} | Intercambios: {swaps:>7}")

def main():
    print("\n" + "="*90)
    print("COMPARACIÓN DE ALGORITMOS DE ORDENAMIENTO (PYTHON) - TIEMPO, COMPARACIONES E INTERCAMBIOS")
    print("="*90)
    
    test_cases = [
        ("aleatoria", generate_random_list),
        ("ordenada", generate_sorted_list),
        ("inversa", generate_reverse_list)
    ]
    
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort)
    ]
    
    for array_type, generator in test_cases:
        print(f"\n=== ARREGLO {array_type.upper()} ===")
        for name, algorithm in algorithms:
            measure_time(algorithm, generator, name, array_type)

if __name__ == "__main__":
    main()