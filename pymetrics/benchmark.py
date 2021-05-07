from collections import namedtuple
import random
random.seed(123)

Benchmark = namedtuple('Benchmark', field_names=['name', 'data'])

mergesort_benchmark = Benchmark(name='mergesort', data=[random.randint(-1000000, 1000000) for _ in range(10000)])

l = 10000
groupby_benchmark = Benchmark(
    name='groupby',
    data={
        'keys': [random.randint(0, 100) for _ in range(l)],
        'values1': [random.randint(-1000000, 1000000) for _ in range(l)],
        'values2': [random.randint(0, 1000000) for _ in range(l)]
    }
)
