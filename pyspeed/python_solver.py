import collections
import pickle
from typing import List, Dict
from benchmark_solver import BenchmarkSolver
import pandas as pd
from datasketch.minhash import MinHash
from datasketch.lsh import MinHashLSH


class PythonSolver(BenchmarkSolver):

    def description(cls):
        return "Pure Python"

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

    def string_slice(self, test_data: Dict):
        string_list: List[str] = test_data["strings"]
        start: int = test_data["start"]
        end: int = test_data["end"]
        return [s[start:end+1] for s in string_list]

    def ngram_count(self, test_data):
        string_list: List[str] = test_data["strings"]
        ngram_n: int = test_data["ngram_n"]
        return [
            count_ngrams(s, ngram_n) for s in string_list
        ]

    def lsh(self, test_data):
        permutations = 100
        lsh = MinHashLSH(threshold=0.5, num_perm=permutations)
        strings = []
        hashes = []
        for i, s in enumerate(test_data["strings"]):
            strings.append(' '.join(s))
            mg = MinHash(permutations)
            for w in s:
                mg.update(w.encode('utf-8'))
            # print(s, mg)
            hashes.append(mg)
            lsh.insert(i, mg, check_duplication=False)
        print("Size:", len(pickle.dumps(lsh)))

        matches = []
        for i in range(len(strings)):
            matches = set(lsh.query(hashes[i])) - {i}
        return matches

def count_ngrams(s, n):
    padded = "$"*(n-1) + s + "$"*(n-1)
    return collections.Counter(padded[i: i + n] for i in range(len(padded) - n + 1))
