import random
from collections import namedtuple

from .benchmark_helpers import alphabet, iter_wikipedia_docs

random.seed(123)

Benchmark = namedtuple("Benchmark", field_names=["name", "data"])


def mergesort_benchmark() -> Benchmark:
    """Mergesort array sorting algorithm.

    Input data: A List[int]
    Expected output: A List[int] sorted ascendingly
    """
    return Benchmark(
        name="mergesort", data=[random.randint(-1000000, 1000000) for _ in range(10000)]
    )


def groupby_sum_benchmark() -> Benchmark:
    """Simple version of a dataframe groupby with sum() aggregation.

    Input data: A dictionary with the following elements:

        - "keys": List[int]  The keys to group by
        - "uints": List[uint] Unsigned integers
        - "ints": List[int] Signed integers

    Expected output: A dictionary with the same keys and value types as before.
        But now the elements in the lists are the sum for all elements with the same
        keys and each key appears only once.
    """
    l = 100000
    return Benchmark(
        name="groupby_sum",
        data={
            "keys": [random.randint(0, 100) for _ in range(l)],
            "ints": [random.randint(-1000000, 1000000) for _ in range(l)],
            "uints": [random.randint(0, 1000000) for _ in range(l)],
            "floats": [(random.random() - 0.5) * 1000 for _ in range(l)],
        },
    )


def string_slice_benchmark() -> Benchmark:
    """Simply take a list of strings and return a slice [n:m] for each.
    Indexing is meant in terms of unicode code points and the strings are unicode.

    Input data: A dictionary with the following elements:

        - "strings": A List[str] with the strings to slice
        - "start": An integer with the index of the first unicode code point to return
        - "end": An integer with the index of the last unicode code point to return

    Expected output: A List[str] with the sliced strings
    """
    allowed_chars = alphabet()

    def rand_string(max_len):
        return "".join(
            random.choice(allowed_chars) for _ in range(random.randint(0, max_len))
        )

    l = 20000
    return Benchmark(
        name="string_slice",
        data={
            "strings": [rand_string(200) for _ in range(l)],
            "start": 105,
            "end": 120,
        },
    )


def ngram_count_benchmark() -> Benchmark:
    """Take a list of strings and count all n-grams of unicode code points

    Input data: A dictionary with:

        - "strings": List[str] with the strings to analyze
        - "ngram_n": int, the length of n-grams to count

    Expected output: A list of dictionaries. Each dictionary should have the form {"n-gram": count}.
    """
    return Benchmark(
        name="ngram_count",
        data={"strings": list(iter_wikipedia_docs(200)), "ngram_n": 3},
    )


def ngram_count_parallel_benchmark() -> Benchmark:
    """Take a list of strings and count all n-grams of unicode code points

    Input data: A dictionary with:

        - "strings": List[str] with the strings to analyze
        - "ngram_n": int, the length of n-grams to count

    Expected output: A list of dictionaries. Each dictionary should have the form {"n-gram": count}.
    """
    return Benchmark(
        name="ngram_count_parallel",
        data={"strings": list(iter_wikipedia_docs(200)), "ngram_n": 3},
    )


def minhash() -> Benchmark:
    """Take a list of string sets and calculate a minhash fingerprint

    Input data: A dictionary with:

        - "shingle_list": List[List[str]] with the strings to analyze
        - "n_hashes": Number of hashes to use

    Expected output: A list of lists of integers (hash values per document).
    """
    shingles = [l.split() for d in iter_wikipedia_docs(200) for l in d.splitlines()]
    return Benchmark(
        name="minhash",
        data={"shingle_list": [s for s in shingles if s], "n_hashes": 64},
    )
