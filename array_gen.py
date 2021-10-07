"""
array_gen.py

A module for generating arrays (lists) of numbers
"""

import random


def gen_sorted_arr(size: int, reverse: bool = False):
    """Generate 
    """
    return sorted((random.random() for i in range(size)), reverse=reverse)

def gen_unsorted_arr(size: int):
    return [random.random() for i in range(size)]

def gen_123_arr(size: int):
    return [random.randint(1, 3) for i in range(size)]

if __name__ == "__main__":
    arr_print = lambda arr: print(*arr, sep='\t')
    arr_print(gen_sorted_arr(8))
    arr_print(gen_sorted_arr(8, True))
    arr_print(gen_unsorted_arr(8))
    arr_print(gen_123_arr(8))

