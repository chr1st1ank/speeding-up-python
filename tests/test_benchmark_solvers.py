
from pyspeed.benchmark_runner import BenchmarkRunner
from pyspeed import benchmark
from pyspeed.benchmark_solver import BenchmarkSolver
from pyspeed.benchmark_result import BenchmarkResult
from pyspeed import python_solver
from pyspeed import numba_solver
from pyspeed import cython_solver
from pyspeed import julia_solver
from pyspeed import cpp_solver
from pyspeed import cpp_pyb11_solver
from pyspeed import rust_solver
import pytest


@pytest.fixture(scope="function", params=[
    python_solver.PythonSolver,
    numba_solver.NumbaSolver,
    cython_solver.CythonSolver,
    julia_solver.JuliaSolver,
    cpp_solver.CppSolver,
    cpp_pyb11_solver.CppPyb11Solver,
    rust_solver.RustSolver

])
def solver(request):
    return request.param()


@pytest.fixture(scope="function")
def runner(solver):
    _runner = BenchmarkRunner(solvers=[
            python_solver.PythonSolver(),
            solver,
        ],
        benchmarks=[benchmark.Benchmark(name='mergesort', data=[1,4,3])]
    )
    yield _runner


def test_mergesort(solver):
    try:
        s = solver.mergesort([1, 5, 3, -1])
    except NotImplementedError:
        pytest.skip("Not implemented")

    assert isinstance(s, list), "Mergesort should return a Python list"
    assert s == [-1, 1, 3, 5]


def test_groupby_sum(solver):
    data_table = {
        "keys": [-5, 10, 4, -5],
        "v1": [1, 2, 3, 4],
        "v2": [-1, -2, -3, -4],
    }
    try:
        p = solver.groupby_sum(data_table)
    except NotImplementedError:
        pytest.skip("Not implemented")
    assert p == {
        "keys": [-5, 4, 10],
        "v1": [5, 3, 2],
        "v2": [-5, -3, -2],
    }


def test_string_slice(solver: BenchmarkSolver):
    data = {
        "strings": [
            "asdfgjkl",
            "奥会多策并举力争实",
            ""
        ],
        "start": 3,
        "end": 7
    }
    try:
        p = solver.string_slice(data)
    except NotImplementedError:
        pytest.skip("Not implemented")
    assert p == [
        "fgjkl",
        "策并举力争",
        ""
    ]


def test_ngram_count(solver: BenchmarkSolver):
    data = {
        "strings": [
            "abac",
            "abcabc",
            "北京",
            ""
        ],
        "ngram_n": 3,
    }
    try:
        p = solver.ngram_count(data)
    except NotImplementedError:
        pytest.skip("Not implemented")
    assert p == [
        {k: 1 for k in ["$$a", "$ab", "aba", "bac", "ac$", "c$$"]},
        {k: (1 if k != "abc" else 2) for k in ["$$a", "$ab", "abc", "bca", "cab", "bc$", "c$$"]},
        {k: 1 for k in ["$$北", "$北京", "北京$", "京$$"]},
        {"$$$": 2}
    ]

def test_solver_results(runner):
    runner.time_it(1, 1)
    assert runner.verify_results()
