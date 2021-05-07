
import typing
import timeit
import random
from benchmark_solver import BenchmarkSolver
from benchmark import Benchmark
from benchmark_result import BenchmarkResult


class BenchmarkRunner:
    def __init__(self, solvers: typing.List[BenchmarkSolver], benchmarks: typing.List[Benchmark]):
        random.seed(123)
        self.solvers = solvers
        self.results = []
        self._benchmarks = {name: data for name, data in benchmarks}
        self.benchmarks = list(self._benchmarks.keys())

    @property
    def solver_names(self):
        return [s.description() for s in self.solvers]

    def verify_results(self):
        for b in self._benchmarks.keys():
            results = list(filter(lambda x: x.benchmark == b, self.results))
            first_result = results[0].solution
            for r in results:
                if r.solution is not None and r.solution != first_result:
                    raise RuntimeError(f"Benchmark '{b}' yields differing result for solver {r.solver}")
        return True

    def time_it(self, repeats=10, number=3):
        for solver in self.solvers:
            print(solver.description())
            for benchmark, input in self._benchmarks.items():
                print(f"\t{benchmark}")
                if not hasattr(solver, benchmark):
                    self.results.append(BenchmarkResult(
                        solver=solver.description(),
                        benchmark=benchmark,
                        time=None,
                        solution=None
                    ))
                else:
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
