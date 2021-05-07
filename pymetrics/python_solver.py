
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

    def mergesort(self, l: List) -> List:
        # return sorted(l)  # Note that Python's sorted() is way faster. But it's a different algorithm and in plain C.
        if len(l) <= 1:
            return l
        left = self.mergesort(l[:int(len(l) / 2)])
        right = self.mergesort(l[int(len(l) / 2):])
        return self.merge(left, right)

    def groupby_sum(self, data_dict):
        # df = pd.DataFrame(data=data)
        # return df.groupby('keys').sum().to_dict(orient='list')
        sorted_keys = sorted(set(data_dict["keys"]))
        output = {
            "keys": sorted_keys
        }
        columns = [c for c in data_dict.keys() if c != "keys"]
        for column in columns:
            output[column] = {k: 0 for k in sorted_keys}
            for k, v in zip(data_dict["keys"], data_dict[column]):
                output[column][k] += v
            output[column] = [output[column][k] for k in sorted_keys]
        return output
