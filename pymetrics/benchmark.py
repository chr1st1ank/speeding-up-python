from collections import namedtuple
import random
random.seed(123)

Benchmark = namedtuple('Benchmark', field_names=['name', 'data'])

mergesort_benchmark = Benchmark(name='mergesort', data=[random.randint(-1000000, 1000000) for _ in range(10000)])

l = 100000
groupby_sum_benchmark = Benchmark(
    name='groupby_sum',
    data={
        'keys': [random.randint(0, 100) for _ in range(l)],
        'uints': [random.randint(-1000000, 1000000) for _ in range(l)],
        'ints': [random.randint(0, 1000000) for _ in range(l)],
        'floats': [(random.random() - 0.5) * 1000  for _ in range(l)]
    }
)
