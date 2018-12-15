import abc
import typing
import timeit
import random
from collections import namedtuple


class BenchmarkSolver:
    @abc.abstractclassmethod
    def description(cls) -> str:
        pass

    @abc.abstractclassmethod
    def direct_dependencies(cls) -> typing.List[str]:
        pass

    @abc.abstractmethod
    def mergesort(cls, input):
        pass


BenchmarkResult = namedtuple('BenchmarkResult', field_names=["solver", "benchmark", "time", "solution"])


class BenchmarkRunner:
    def __init__(self, solvers: typing.List[BenchmarkSolver]):
        self.solvers = solvers
        self.results = []
        self._benchmarks = {
            'mergesort': [random.randint(-1000000, 1000000) for _ in range(10000)]
        }
        self.benchmarks = list(self._benchmarks.keys())

    @property
    def solver_names(self):
        return [s.description() for s in self.solvers]

    def verify_results(self):
        for b in self._benchmarks.keys():
            results = list(filter(lambda x: x.benchmark==b, self.results))
            first_result = results[0].solution
            for r in results:
                if r.solution != first_result:
                    raise RuntimeError(f"Benchmark '{b}' yields differing result for solver {r.solver}")
        return True

    def time_it(self, repeats=10, number=3):
        for solver in self.solvers:
            print(solver.description())
            for benchmark, input in self._benchmarks.items():
                print(f"\t{benchmark}")
                f = getattr(solver, benchmark)
                timer =timeit.Timer('f(input)', globals=dict(f=f, input=input), )
                t = timer.repeat(repeat=repeats, number=number)
                sol = f(input)
                self.results.append(BenchmarkResult(
                    solver=solver.description(),
                    benchmark=benchmark,
                    time=min(t),
                    solution=sol
                ))
