import random
import time
from typing import Callable, Dict, List
from dataclasses import dataclass
from functools import partial
import csv

import matplotlib.pyplot as plt

from array_gen import gen_unsorted_arr,  gen_sorted_arr, gen_123_arr
from sort_algos import selection_sort, insertion_sort, merge_sort, shellsort

SIZES = [i for i in range(7, 15)]

@dataclass
class ExpRes:
    """The class represents the result of an experiment (sorting an array)"""
    elapsed_time: float
    num_compares: int
    def __add__(self, other: "ExpRes"):
        return ExpRes(self.elapsed_time + other.elapsed_time,
                    self.num_compares + other.num_compares)
    def __truediv__(self, num: float):
        return ExpRes(self.elapsed_time / num,
                    self.num_compares // num)

def run_single_sort(algorithm: Callable, arr: list):
    start = time.time()
    num_compares = algorithm(arr)
    elapsed = time.time() - start
    return ExpRes(elapsed_time=elapsed, num_compares=num_compares)

def experiment_on_random(size: int, algorithms: List[Callable]):
    num_repeats = 5
    arrays = [gen_unsorted_arr(2**size) for _ in range(num_repeats)]
    algorithm_result_dict = {}
    for algorithm in algorithms:
        result = ExpRes(0, 0)
        for arr in arrays:
            result += run_single_sort(algorithm, arr.copy())
        result =  result / num_repeats
        algorithm_result_dict[algorithm.__name__] = result
    return algorithm_result_dict

def experiment_on_sorted(size: int, algorithms: List[Callable], reverse: bool):
    arr = gen_sorted_arr(2**size, reverse=reverse)
    algorithm_result_dict = {}
    for algorithm in algorithms:
        algorithm_result_dict[algorithm.__name__] = run_single_sort(algorithm, arr.copy())
    return algorithm_result_dict

def experiment_on_123(size: int, algorithms: List[Callable]):
    num_repeats = 3
    arr = gen_123_arr(2**size)
    algorithm_result_dict = {}
    for algorithm in algorithms:
        result = ExpRes(0, 0)
        for _ in range(num_repeats):
            random.shuffle(arr)
            result += run_single_sort(algorithm, arr.copy())
        result = result / num_repeats
        algorithm_result_dict[algorithm.__name__] = result
    return algorithm_result_dict

def run_all_experiments():
    result_table = []
    for experiment, experiment_name in zip([experiment_on_random, partial(experiment_on_sorted, reverse=False),
                        partial(experiment_on_sorted, reverse=True), experiment_on_123],
                        ['Random array', 'Sorted array', 'Reversed array', 'Array with many repetitions']):
        for size in SIZES:
            algorithm_result_dict = experiment(size, [selection_sort, insertion_sort, merge_sort, shellsort])
            result_table.extend([[experiment_name, algorithm, size, res.elapsed_time, res.num_compares] for algorithm, res in algorithm_result_dict.items()])

    return result_table

def visualize(result_table):
    experiment_algorithm_dict = {}
    for experiment, algorithm, size, elapsed, num_compares in result_table:
        experiment_algorithm_dict.setdefault(experiment, {}).setdefault(algorithm, []).append([size, elapsed, num_compares])
    for experiment in experiment_algorithm_dict:
        for algorithm in experiment_algorithm_dict[experiment]:
            experiment_algorithm_dict[experiment][algorithm].sort()
            size_elapsed_num_compares = experiment_algorithm_dict[experiment][algorithm]
            plt.plot([i[0] for i in size_elapsed_num_compares], [1000*i[1] for i in size_elapsed_num_compares], label=algorithm)
        plt.legend()
        plt.title(experiment)
        plt.yscale('log')
        plt.xlabel("Size of array, 2^x elements")
        plt.ylabel("Elapsed time, ms")
        plt.show()
        for algorithm in experiment_algorithm_dict[experiment]:
            experiment_algorithm_dict[experiment][algorithm].sort()
            size_elapsed_num_compares = experiment_algorithm_dict[experiment][algorithm]
            plt.plot([i[0] for i in size_elapsed_num_compares], [1000*i[1] for i in size_elapsed_num_compares], label=algorithm)
        plt.legend()
        plt.title(experiment)
        plt.yscale('log')
        plt.xlabel("Size of array, 2^x elements")
        plt.ylabel("Number of compares")
        plt.show()


if __name__ == "__main__":
    visualize(run_all_experiments())
