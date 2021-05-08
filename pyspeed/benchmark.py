from collections import namedtuple
import random

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


def string_slice_benchmark() -> Benchmark:
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

    allowed_chars = ''.join(
        chr(code_point) * weight
        for range_start, range_end, weight in include_ranges
        for code_point in range(range_start, range_end + 1)
    )

    def rand_string(max_len):
        return ''.join(random.choice(allowed_chars) for _ in range(random.randint(0, max_len)))

    l = 200000
    return Benchmark(
        name="string_slice",
        data={
            "strings": [rand_string(50) for _ in range(l)],
            "start": 5,
            "end": 20
        }
    )
