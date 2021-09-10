from collections import namedtuple


BenchmarkResult = namedtuple(
    "BenchmarkResult", field_names=["solver", "benchmark", "time", "solution"]
)
