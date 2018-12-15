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
from typing import List
import numba

from benchmark import BenchmarkSolver


@numba.jit(nopython=True)
def merge(l: List, r: List) -> List:
    result = []

    while len(l) and len(r):
        if l[0] <= r[0]:
            result.append(l.pop(0))
        else:
            result.append(r.pop(0))
    if l:
        return result + l
    if r:
        return result + r

    return result


@numba.jit(nopython=True)
def mergesort(l: List) -> List:
    if len(l) <= 1:
        return l
    left = mergesort(l[:int(len(l) / 2)])
    right = mergesort(l[int(len(l) / 2):])
    return merge(left, right)


class NumbaSolver(BenchmarkSolver):
    def __init__(self):
        # Run once to cache compilation
        self.mergesort([1,4,2])
        pass

    def description(cls):
        return "Numba"

    def direct_dependencies(cls):
        return ['numba']

    def mergesort(cls, input):
        return mergesort(input)
