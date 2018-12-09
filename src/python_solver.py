
from typing import List
from benchmark import BenchmarkSolver


class PythonSolver(BenchmarkSolver):

    def description(cls):
        return "Pure Python"

    def direct_dependencies(cls):
        return []

    @staticmethod
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

    @staticmethod
    def mergesort(l: List) -> List:
        if len(l) <= 1:
            return l
        left = PythonSolver.mergesort(l[:int(len(l) / 2)])
        right = PythonSolver.mergesort(l[int(len(l) / 2):])
        return PythonSolver.merge(left, right)
