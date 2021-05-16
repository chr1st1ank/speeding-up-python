"""Rust implementation

Notes:
    * The functions to be compiled have to be in a separate file with *.so ending.
"""
import pyspeed_rust

from benchmark_solver import BenchmarkSolver
from typing import List, Dict


class RustSolver(BenchmarkSolver):
    def description(cls):
        return "Rust"

    def mergesort(self, l: List) -> List:
        return pyspeed_rust.mergesort(l)

    def groupby_sum(self, data):
        return pyspeed_rust.groupby_sum(data)

    def string_slice(self, test_data: Dict):
        string_list: List[str] = test_data["strings"]
        start: int = test_data["start"]
        end: int = test_data["end"]
        return pyspeed_rust.string_slice(string_list, start, end)

    def ngram_count(self, test_data):
        string_list: List[str] = test_data["strings"]
        ngram_n: int = test_data["ngram_n"]
        return pyspeed_rust.count_ngrams_list(string_list, ngram_n)

    def ngram_count_parallel(self, test_data):
        string_list: List[str] = test_data["strings"]
        ngram_n: int = test_data["ngram_n"]
        return pyspeed_rust.count_ngrams_list_parallel(string_list, ngram_n)
