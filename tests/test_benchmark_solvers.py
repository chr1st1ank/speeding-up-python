
from benchmark import BenchmarkRunner
import python_solver
import numba_solver
import cython_solver
import julia_solver
import pytest


@pytest.fixture(scope="module", params=[
    numba_solver.NumbaSolver,
    cython_solver.CythonSolver,
    julia_solver.JuliaSolver
])
def solver(request):
    return request.param()


@pytest.fixture(scope="module")
def runner(solver):
    _runner = BenchmarkRunner(solvers=[
        python_solver.PythonSolver(),
        solver
    ])
    yield _runner


def test_mergesort(solver):
    s = solver.mergesort([1, 5, 3, -1])

    assert isinstance(s, list), "Mergesort should return a Python list"
    assert s == [-1, 1, 3, 5]


def test_solver_results(runner):
    runner.time_it(1, 1)
    assert runner.verify_results()
