
from typing import List
from benchmark_solver import BenchmarkSolver
import pandas as pd


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
        #return sorted(l)  # Note that Python's sorted() is way faster. But it's a different algorithm and in plain C.
        if len(l) <= 1:
            return l
        left = PythonSolver.mergesort(l[:int(len(l) / 2)])
        right = PythonSolver.mergesort(l[int(len(l) / 2):])
        return PythonSolver.merge(left, right)

    @staticmethod
    def groupby(data):
        df = pd.DataFrame(data=data)
        return df.groupby('keys').sum().to_dict(orient='index')
