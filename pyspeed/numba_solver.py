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
import numba
from numba import int64
from numba.typed import Dict, List

from benchmark_solver import BenchmarkSolver


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
    left = mergesort(l[:int(len(l) / 2)])
    right = mergesort(l[int(len(l) / 2):])
    return merge(left, right)

@numba.jit(nopython=True)
def count_ngrams(string_list: List[str], n: numba.int32):
    all_counts = List()
    for s in string_list:
        padded = "$" * (n - 1) + s + "$" * (n - 1)
        counts = Dict()
        for i in range(len(padded) - n + 1):
            k = padded[i: i + n]
            if k in counts:
                counts[k] += 1
            else:
                counts[k] = 1
        all_counts.append(counts)
    return all_counts

class NumbaSolver(BenchmarkSolver):
    def __init__(self):
        # Run once to cache compilation
        l = List()
        [l.append(x) for x in [1, 4, 2]]
        self.mergesort(l)
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

    # @staticmethod
    # def groupby_sum(data):
    #     keys = set(data['keys'])
    #     results = {
    #         key: {
    #             'values1': 0,
    #             'values2': 0
    #         } for key in keys
    #     }
    #     for i in enumerate
    #     df = pd.DataFrame(data=data)
    #     return df.groupby('keys').sum().to_dict(orient='index')
