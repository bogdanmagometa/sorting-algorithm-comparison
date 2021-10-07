"""
sort_algos.py

The module contains implementation of the following sorting algorithms:
1. insertion_sort
2. selection_sort
3. shell_sort
4. merge_sort
Each of the listed above functions returns number of compares made after
beeing invoked.
"""

def insertion_sort(arr):
    """In-place insertion sort. Return number of compares"""
    num_compares = 0
    def inc_compares():
        nonlocal num_compares
        num_compares += 1
        return False

    for i in range(1, len(arr)):
        key = arr[i]
        j = i
        while j > 0 and (inc_compares() or arr[j-1] > key):
            arr[j] = arr[j-1]
            j -= 1
        arr[j] = key

    return num_compares

def selection_sort(arr):
    """In-place selection sort. Return number of compares"""
    num_compares = 0

    n = len(arr)
    for i in range(n-1):
        min = i
        for j in range(i+1, n):
            num_compares += 1
            if arr[j] < arr[min]:
                min = j
        arr[i], arr[min] = arr[min], arr[i]
    return num_compares

def shellsort(arr):
    """In-place shellsort. Return number of compares"""
    num_compares = 0
    def inc_compares():
        nonlocal num_compares
        num_compares += 1
        return False

    step = 1
    while step < len(arr) / 3:
        step = 3*step + 1
    while step >= 1:
        for i in range(step, len(arr)):
            j = i
            key = arr[j]
            while j >= step and (inc_compares() or  arr[j-step] > key):
                arr[j] = arr[j-step]
                j -= step
            arr[j] = key
        step //= 3
    return num_compares

def merge_sort(arr):
    """In-place merge sort. Return number of compares"""
    return _merge_sort(arr, 0, len(arr) - 1)

def _merge_sort(arr, start: int, end: int):
    num_compares = 0

    if start < end:
        mid = (start + end) // 2
        num_compares += _merge_sort(arr, start, mid)
        num_compares += _merge_sort(arr, mid + 1, end)
        num_compares += _merge(arr, start, mid, end)

    return num_compares

def _merge(arr, start: int, mid: int, end: int):
    num_compares = 0
    left = [arr[i] for i in range(start, mid + 1)]
    left.append(float('inf'))
    right = [arr[i] for i in range(mid + 1, end + 1)]
    right.append(float('inf'))
    i, j = 0, 0
    for k in range(start, end+1):
        if float('inf') not in [left[i], right[j]]:
            num_compares += 1
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1

    return num_compares

if __name__ == "__main__":
    arr = [8, 1, 41, 1, 0, -1, 0]
    #insertion_sort(arr)
    #selection_sort(arr)
    shellsort(arr)
    #merge_sort(arr)
    print(arr)
