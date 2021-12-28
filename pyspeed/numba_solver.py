"""Implementation in Python, accelerated by the JIT compilation with Numba

Prerequisites:
    * Only numba has to be installed, afterwards pure Python functions can be compiled just-in-time with the @jit
      decorator

Notes:
    * Individual methods of Python classes cannot be compiled with the fast "nopython" mode, but the very slow
      "object" mode has to be used.
    * Entire Python classes could be compiled, but not if they inherit from a pure Python class which is not compiled
      with Numba
"""
import binascii

import numba
from numba import int64
from numba.typed import Dict, List
import numpy as np

from .benchmark_solver import BenchmarkSolver


@numba.jit(nopython=True)
def merge(l: List[int64], r: List[int64]) -> List[int64]:
    result: List[int64] = List()

    while len(l) and len(r):
        if l[0] <= r[0]:
            result.append(l.pop(0))
        else:
            result.append(r.pop(0))
    if l:
        for i in l:
            result.append(i)
    if r:
        for i in r:
            result.append(i)

    return result


@numba.jit(nopython=True)
def mergesort(l: List[int64]) -> List[int64]:
    if len(l) <= 1:
        return l
    left = mergesort(l[: int(len(l) / 2)])
    right = mergesort(l[int(len(l) / 2) :])
    return merge(left, right)


@numba.jit(nopython=True)
def count_ngrams(string_list: List[str], n: numba.int32):
    all_counts = List()
    for s in string_list:
        padded = "$" * (n - 1) + s + "$" * (n - 1)
        counts = Dict()
        for i in range(len(padded) - n + 1):
            k = padded[i : i + n]
            if k in counts:
                counts[k] += 1
            else:
                counts[k] = 1
        all_counts.append(counts)
    return all_counts


@numba.jit(nopython=False)
def fix_array_or_list(l):
    if not l:
        List.empty_list(str)
    dt = numba.typeof(l[0])
    new_list = List.empty_list(dt)
    for x in l:
        new_list.append(x)
    return new_list

_mersenne_prime = np.uint32((1 << 32) - 1)
_max_hash = np.uint32((1 << 32) - 1)


def hash32(data):
    return binascii.crc32(data) & 0xffffffff


@numba.jit(nopython=True)
def permutate_and_take_min(h: np.array, A: np.array, B: np.array) -> np.array:
    hashes = h.repeat(A.shape[0]).reshape(h.shape[0], A.shape[0])
    hashes = (A * hashes + B) % _mersenne_prime
    # minhashes = np.empty(hashes.shape[1])
    # for i in range(hashes.shape[1]):
    #     minhashes[i] = hashes[:, i].min()
    minhashes = [hashes[:, i].min() for i in range(hashes.shape[1])]
    return minhashes


# @numba.jit(nopython=False)
def calc_minhashes(shingles: List[str], A: np.array, B: np.array) -> np.array:
    hashes = np.array(
        [hash32(s.encode("utf-8")) for s in shingles], dtype=np.uint32
    )
    return permutate_and_take_min(hashes, A, B)

def hash_primes(n_hashes: int, random_seed: int):
    gen = np.random.RandomState(random_seed)
    A = gen.randint(1, _mersenne_prime, size=n_hashes, dtype='uint32')
    B = gen.randint(0, _mersenne_prime, size=n_hashes, dtype='uint32')
    return A, B


class NumbaSolver(BenchmarkSolver):
    def __init__(self):
        # Run once to cache compilation
        l = List()
        [l.append(x) for x in [1, 4, 2]]
        self.mergesort(l)
        self.ngram_count({"strings": ["A"], "ngram_n": 1})
        pass

    def description(self):
        return "Numba"

    def mergesort(self, input):
        l = List()
        [l.append(x) for x in input]
        return list(mergesort(l))

    def ngram_count(self, test_data):
        string_list: List[str] = test_data["strings"]
        ngram_n: int = test_data["ngram_n"]
        return list(count_ngrams(string_list, ngram_n))
        # return list(count_ngrams(fix_array_or_list(string_list), ngram_n))

    # For some reason this gives wrong results as soon as the code is compiled with numba
    # def minhash(self, test_data):
    #     shingle_list: List[List[str]] = test_data["shingle_list"]
    #     n_hashes: int = test_data["n_hashes"]
    #     A, B = hash_primes(n_hashes=n_hashes, random_seed=42)
    #     return [
    #         calc_minhashes(shingles, A, B) for shingles in shingle_list
    #     ]
