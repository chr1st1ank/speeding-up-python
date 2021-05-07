"""Rust implementation

Notes:
    * The functions to be compiled have to be in a separate file with *.so ending.
"""
import pyspeed_rust

from benchmark_solver import BenchmarkSolver
from typing import List

class RustSolver(BenchmarkSolver):
    def description(cls):
        return "Rust from Python"

    def mergesort(self, l: List) -> List:
        return pyspeed_rust.mergesort(l)

    # @staticmethod
    # def groupby_sum(data):
    #     return cython_backend.groupby_sum_cy(data)
