"""
array_gen.py

A module for generating arrays (lists) of numbers
"""

import random

MIN_ELEMENT = -2**15
MAX_ELEMENT = 2**15

def gen_sorted_arr(size: int, reverse: bool = False):
    """Generate 
    """
    return sorted((random.randint(MIN_ELEMENT, MAX_ELEMENT) for i in range(size)), reverse=reverse)

def gen_unsorted_arr(size: int):
    return [random.randint(MIN_ELEMENT, MAX_ELEMENT) for i in range(size)]

def gen_123_arr(size: int):
    return [random.randint(1, 3) for i in range(size)]

if __name__ == "__main__":
    arr_print = lambda arr: print(*arr, sep='\t')
    arr_print(gen_sorted_arr(8))
    arr_print(gen_sorted_arr(8, True))
    arr_print(gen_unsorted_arr(8))
    arr_print(gen_123_arr(8))

