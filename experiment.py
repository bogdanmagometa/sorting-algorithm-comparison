"""
experiment.py

This is a module for running the sorting algrithms on different arrays and
visualizing the results.
"""

import random
import time
from typing import Callable, Dict, List
from dataclasses import dataclass
from functools import partial

import matplotlib.pyplot as plt

from array_gen import gen_unsorted_arr,  gen_sorted_arr, gen_123_arr
from sort_algos import selection_sort, insertion_sort, merge_sort, shellsort

SIZES = [i for i in range(7, 16)]

@dataclass
class ExpRes:
    """The class represents the result of an experiment
    (sorting an array)"""
    elapsed_time: float
    num_compares: int
    def __add__(self, other: "ExpRes"):
        return ExpRes(self.elapsed_time + other.elapsed_time,
                    self.num_compares + other.num_compares)
    def __truediv__(self, num: float):
        return ExpRes(self.elapsed_time / num,
                    self.num_compares // num)

def run_single_sort(algorithm: Callable, arr: list) -> ExpRes:
    """Run a specified sorting algorithm on a specified array (list) of
    elements.
    Return result of experiment: elapsed time and number of compares.
    """
    start = time.time()
    num_compares = algorithm(arr)
    elapsed = time.time() - start
    return ExpRes(elapsed_time=elapsed, num_compares=num_compares)

def experiment_on_random(size: int, algorithms: List[Callable]):
    """Run experiment #1 (the order of elements in array is random) on
    array of specified length for each algorithm specified.
    Return a dictionary. Each key is some sorting algorithm. Each value is
    a result of experiment #1 using some sorting algorithm.
    """
    num_repeats = 5
    arrays = [gen_unsorted_arr(2**size) for _ in range(num_repeats)]
    algorithm_result_dict = {}
    for algorithm in algorithms:
        result = ExpRes(0, 0)
        for arr in arrays:
            result += run_single_sort(algorithm, arr.copy())
        result =  result / num_repeats
        algorithm_result_dict[algorithm] = result
    return algorithm_result_dict

def experiment_on_sorted(size: int, algorithms: List[Callable], reverse: bool):
    """Run specified algorithms on sorted array of specified length.
    Return a dictionary. Each key is some sorting algorithm. Each value is
    a result of the experiment using some sorting algorithm.
    """
    arr = gen_sorted_arr(2**size, reverse=reverse)
    algorithm_result_dict = {}
    for algorithm in algorithms:
        algorithm_result_dict[algorithm] = run_single_sort(algorithm,
                                                                arr.copy())
    return algorithm_result_dict

def experiment_on_123(size: int, algorithms: List[Callable]):
    """Run specified algorithms on array of specified length with many
    repetitions of 1, 2 and 3.
    Return a dictionary. Each key is some sorting algorithm. Each value
    is a result of the experiment using some sorting algorithm.
    """
    num_repeats = 3
    arr = gen_123_arr(2**size)
    algorithm_result_dict = {}
    for algorithm in algorithms:
        result = ExpRes(0, 0)
        for _ in range(num_repeats):
            random.shuffle(arr)
            result += run_single_sort(algorithm, arr.copy())
        result = result / num_repeats
        algorithm_result_dict[algorithm] = result
    return algorithm_result_dict

def run_all_experiments():
    """Conduct all experiments and return a list of results.
    """
    result_table = []
    for experiment, experiment_name in zip([experiment_on_random,
                    partial(experiment_on_sorted, reverse=False),
                    partial(experiment_on_sorted, reverse=True),
                    experiment_on_123],
                    ['Random array', 'Sorted array',
                    'Reversed array', 'Array with many repetitions']):
        for size in SIZES:
            algorithm_result_dict = experiment(size, [selection_sort,
                                    insertion_sort, merge_sort, shellsort])
            for algorithm, res in algorithm_result_dict.items():
                result_table.append([experiment_name, algorithm, size,
                                res.elapsed_time, res.num_compares])

    return result_table

def visualize(result_table, algorithm_to_name: dict):
    """Visualize the results of experiments.
    """
    experiment_algorithm_dict = {}
    for experiment, algorithm, size, elapsed, num_compares in result_table:
        experiment_algorithm_dict.setdefault(experiment, {}).setdefault(algorithm, []).append([size, elapsed, num_compares])
    for experiment in experiment_algorithm_dict:
        for algorithm in experiment_algorithm_dict[experiment]:
            experiment_algorithm_dict[experiment][algorithm].sort()
            size_elapsed_num_compares = experiment_algorithm_dict[experiment][algorithm]
            plt.plot([i[0] for i in size_elapsed_num_compares],
                    [1000*i[1] for i in size_elapsed_num_compares],
                    label=algorithm_to_name[algorithm])
        plt.legend()
        plt.title(experiment)
        plt.yscale('log', base=2)
        plt.xlabel("Size of array, 2^x elements")
        plt.ylabel("Elapsed time, ms")
        plt.savefig(f"{experiment[:4]}_elapsed.png")
        plt.clf()
        for algorithm in experiment_algorithm_dict[experiment]:
            experiment_algorithm_dict[experiment][algorithm].sort()
            size_elapsed_num_compares = experiment_algorithm_dict[experiment][algorithm]
            plt.plot([i[0] for i in size_elapsed_num_compares],
                    [1000*i[2] for i in size_elapsed_num_compares],
                    label=algorithm_to_name[algorithm])
        plt.legend()
        plt.title(experiment)
        plt.yscale('log', base=2)
        plt.xlabel("Size of array, 2^x elements")
        plt.ylabel("Number of compares")
        plt.savefig(f"{experiment[:4]}_num_compares.png")
        plt.clf()


if __name__ == "__main__":
    algorithm_to_name = {selection_sort: "Selection sort",
                        insertion_sort : "Insertion sort",
                        merge_sort: "Merge sort", shellsort: "Shellsort"}
    visualize(run_all_experiments(), algorithm_to_name)
