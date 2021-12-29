"""Rust implementation

Notes:
    * The functions to be compiled have to be in a separate file with *.so ending.
"""
from typing import List, Dict

import numpy as np

from . import pyspeed_rust
from .benchmark_solver import BenchmarkSolver


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
        # return pyspeed_rust.count_ngrams_list_native(string_list, ngram_n)
        return pyspeed_rust.count_ngrams_list(string_list, ngram_n)

    def ngram_count_parallel(self, test_data):
        string_list: List[str] = test_data["strings"]
        ngram_n: int = test_data["ngram_n"]
        return pyspeed_rust.count_ngrams_list_parallel(string_list, ngram_n)

    def minhash(self, test_data):
        shingle_list: List[List[str]] = test_data["shingle_list"]
        n_hashes: int = test_data["n_hashes"]
        return minhash(shingle_list, n_hashes, 42)


_mersenne_prime = np.uint32((1 << 32) - 1)


def minhash(shingle_list, n_hashes, random_seed):
    gen = np.random.RandomState(random_seed)
    a = gen.randint(1, _mersenne_prime, size=n_hashes, dtype='uint32')
    b = gen.randint(0, _mersenne_prime, size=n_hashes, dtype='uint32')

    return [
        [int(h) for h in pyspeed_rust.calc_minhashes(shingles, a, b)] for shingles in shingle_list
    ]
