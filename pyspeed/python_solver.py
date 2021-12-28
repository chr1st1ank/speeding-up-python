import binascii
import collections
from typing import List, Dict, Set

import murmurhash.mrmr
import numpy as np
from joblib import Parallel, delayed

from .benchmark_solver import BenchmarkSolver


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
        left = self.mergesort(l[: int(len(l) / 2)])
        right = self.mergesort(l[int(len(l) / 2) :])
        return self.merge(left, right)

    def groupby_sum(self, data_dict):
        # df = pd.DataFrame(data=data)
        # return df.groupby('keys').sum().to_dict(orient='list')
        sorted_keys = sorted(set(data_dict["keys"]))
        output = {"keys": sorted_keys}
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
        return [s[start : end + 1] for s in string_list]

    def ngram_count(self, test_data):
        string_list: List[str] = test_data["strings"]
        ngram_n: int = test_data["ngram_n"]
        return [count_ngrams(s, ngram_n) for s in string_list]

    def ngram_count_parallel(self, test_data):
        string_list: List[str] = test_data["strings"]
        ngram_n: int = test_data["ngram_n"]
        return Parallel(n_jobs=3)(
            delayed(count_ngrams)(s, ngram_n) for s in string_list
        )

    def minhash(self, test_data):
        shingle_list: List[List[str]] = test_data["shingle_list"]
        n_hashes: int = test_data["n_hashes"]
        mh_gen = make_minhash_generator(n_hashes=n_hashes)
        return [
            list(map(int, mh_gen(shingles))) for shingles in shingle_list
        ]


def count_ngrams(s, n):
    padded = "$" * (n - 1) + s + "$" * (n - 1)
    return collections.Counter(padded[i : i + n] for i in range(len(padded) - n + 1))




def make_minhash_generator(n_hashes=100, random_seed=42):
    _mersenne_prime = np.uint32((1 << 32) - 1)
    _max_hash = np.uint32((1 << 32) - 1)
    gen = np.random.RandomState(random_seed)
    A = gen.randint(1, _mersenne_prime, size=n_hashes, dtype='uint32')
    B = gen.randint(0, _mersenne_prime, size=n_hashes, dtype='uint32')

    def hash32(data):
        return murmurhash.mrmr.hash(data)

    def calc_minhashes(shingles: List[str]) -> np.array:
        hashes = np.array(
            [hash32(s.encode("utf-8")) for s in shingles], dtype=np.uint32
        )
        hashes = hashes.repeat(A.shape[0]).reshape(hashes.shape[0], A.shape[0])
        hashes = ((A * hashes + B) % _mersenne_prime) & _max_hash
        minhashes = np.min(hashes, axis=0)
        return minhashes

    return calc_minhashes
