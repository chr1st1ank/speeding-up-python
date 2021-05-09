import pathlib
from collections import namedtuple
import random
from functools import lru_cache

random.seed(123)

Benchmark = namedtuple('Benchmark', field_names=['name', 'data'])

def mergesort_benchmark() -> Benchmark:
    return Benchmark(name='mergesort', data=[random.randint(-1000000, 1000000) for _ in range(10000)])


def groupby_sum_benchmark() -> Benchmark:
    l = 100000
    return Benchmark(
        name='groupby_sum',
        data={
            'keys': [random.randint(0, 100) for _ in range(l)],
            'uints': [random.randint(-1000000, 1000000) for _ in range(l)],
            'ints': [random.randint(0, 1000000) for _ in range(l)],
            # 'floats': [(random.random() - 0.5) * 1000  for _ in range(l)]
        }
    )


@lru_cache()
def alphabet():
    include_ranges = [
        (0x0021, 0x0021, 1),
        (0x0023, 0x0026, 1),
        (0x0028, 0x007E, 100),
        (0x00A1, 0x00AC, 1),
        (0x00AE, 0x00FF, 1),
        (0x0100, 0x017F, 1),
        (0x0180, 0x024F, 1),
        (0x2C60, 0x2C7F, 1),
        (0x16A0, 0x16F0, 1),
        (0x0370, 0x0377, 1),
        (0x037A, 0x037E, 1),
        (0x0384, 0x038A, 1),
        (0x038C, 0x038C, 1),
    ]

    return ''.join(
        chr(code_point) * weight
        for range_start, range_end, weight in include_ranges
        for code_point in range(range_start, range_end + 1)
    )


def string_slice_benchmark() -> Benchmark:
    allowed_chars = alphabet()

    def rand_string(max_len):
        return ''.join(random.choice(allowed_chars) for _ in range(random.randint(0, max_len)))

    l = 20000
    return Benchmark(
        name="string_slice",
        data={
            "strings": [rand_string(200) for _ in range(l)],
            "start": 105,
            "end": 120
        }
    )


@lru_cache()
def load_txt(pathlib_obj):
    with pathlib_obj.open('r') as f:
        return f.read()

def iter_wikipedia_docs(max_docs=1000):
    data_path = pathlib.Path(__file__).parent.parent / 'data' / 'wikipediaArticles'
    for i, p in enumerate(data_path.glob('*.txt')):
        if i > max_docs:
            break
        yield load_txt(p)

def ngram_count_benchmark() -> Benchmark:
    # allowed_chars = alphabet()
    #
    # def rand_string(max_len):
    #     return ''.join(random.choice(allowed_chars) for _ in range(random.randint(0, max_len)))

    # l = 10
    # return Benchmark(
    #     name="ngram_count",
    #     data={
    #         "strings": l*[rand_string(20000)],
    #         "ngram_n": 3
    #     }
    # )

    return Benchmark(
        name="ngram_count",
        data={
            "strings": list(iter_wikipedia_docs(100)),
            "ngram_n": 3
        }
    )
