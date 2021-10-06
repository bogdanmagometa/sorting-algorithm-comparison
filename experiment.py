import random
from typing import Callable, Dict
from dataclasses import dataclass

import matplotlib.pyplot as plt
import timeit

from array_gen import gen_unsorted_arr,  gen_sorted_arr, gen_123_arr
from sort_algos import selection_sort, insertion_sort, merge_sort, shell_sort

SIZES = [2**i for i in range(7, 16)]

@dataclass
class ExpRes:
    """The class represents the result of an experiment (sorting an array)"""
    time: float
    num_compares: int

def test_on_unsorted_arr(algorithms: List[Callable]) -> Dict[int, float]:
    size_time_dict = {}
    num_repetitions = 5
    for size in SIZES:
        code_to_exec = f"{algorithm.__name__}(arr)"
        setup_code = f"from array_gen import gen_unsorted_arr\n"\
                    f"from sort_algos import {algorithm.__name__}\n"\
                    f"arr = gen_unsorted_arr({size})"
        exec_time = timeit.timeit(code_to_exec, setup=setup_code, number=num_repetitions)
        average = exec_time / num_repetitions
        size_time_dict[size] = average

    return size_time_dict

def test_on_sorted_arr(algorithm, reverse: bool):
    size_time_dict = {}
    for size in SIZES:
        code_to_exec = f"{algorithm.__name__}(arr)"
        setup_code = f"from array_gen import gen_sorted_arr\n"\
                    f"from sort_algos import {algorithm.__name__}\n"\
                    f"arr = gen_sorted_arr({size}, reverse={reverse})"
        size_time_dict[size] = timeit.timeit(code_to_exec, setup=setup_code, number=1)

    return size_time_dict

def test_on_repeating_elements(algorithm):
    size_time_dict = {}
    for size in SIZES:
        num_repetitions = 3
        arr = gen_123_arr(size)
        average = 0
        for i in range(num_repetitions):
            random.shuffle(arr)
            average += timeit.timeit(lambda: algorithm(arr), number=1)
        average /= num_repetitions
        size_time_dict[size] = average

    return size_time_dict

if __name__ == "__main__":
    print(test_on_unsorted_arr(shell_sort))
    print(test_on_sorted_arr(shell_sort, False))
    print(test_on_sorted_arr(shell_sort, True))
    print(test_on_repeating_elements(shell_sort))
