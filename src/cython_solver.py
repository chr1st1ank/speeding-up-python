import cython
from Cython.Build import cythonize
# import pyximport; pyximport.install(language_level=3)


from typing import List
from benchmark import BenchmarkSolver


class CythonSolver(BenchmarkSolver):
    def __init__(self):
        # Run once to cache compilation
        self.mergesort([1,4,2])
        pass

    def description(cls):
        return "Cythonized Python"

    def direct_dependencies(cls):
        return ['cython']

    def merge_cy(self, l, r):
        """Returns a sorted list with all elements from l and r"""
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

    @cy
    def mergesort(self, l):
        cdef int x = len(l)
        if x <= 1:
            return l
        x /= 2
        left = self.mergesort(l[:x])
        right = self.mergesort(l[x:])
        return self.merge_cy(left, right)

# mergesort = cythonize("mergesort.pyx")