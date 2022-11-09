import platform
from collections import Counter

from pyspeed import benchmark
from pyspeed import cpp_pyb11_solver
from pyspeed import cpp_solver
from pyspeed import cython_solver
# from pyspeed import julia_solver
# from pyspeed import numba_solver
from pyspeed import python_solver
from pyspeed import rust_solver
from pyspeed.benchmark_runner import BenchmarkRunner


def system_info():
    print("\nSystem information:\n")

    # Architecture
    print(f"Architecture: {platform.machine()} / {platform.architecture()[0]}")
    print(f"System: {platform.system()} / {platform.release()}")
    print(
        f"Python: {platform.python_implementation()} {platform.python_version()} built with {platform.libc_ver()}"
    )

    print("Processors: ")
    try:
        with open("/proc/cpuinfo", "r") as f:
            cpu_info = Counter(
                [x.strip().split(":")[1] for x in f.readlines() if "model name" in x]
            )
            for name, count in cpu_info.items():
                print(f"    {count} x {name}")
    except:
        print(platform.processor())  # May return empty string!


if __name__ == "__main__":
    system_info()

    runner = BenchmarkRunner(
        solvers=[
            python_solver.PythonSolver(),
            # numba_solver.NumbaSolver(),
            cython_solver.CythonSolver(),
            # julia_solver.JuliaSolver(),
            cpp_solver.CppSolver(),
            cpp_pyb11_solver.CppPyb11Solver(),
            rust_solver.RustSolver(),
        ],
        benchmarks=[
            benchmark.mergesort_benchmark(),
            benchmark.groupby_sum_benchmark(),
            benchmark.string_slice_benchmark(),
            benchmark.ngram_count_benchmark(),
            benchmark.ngram_count_parallel_benchmark(),
            benchmark.minhash(),
        ],
    )
    runner.time_it()
    runner.verify_results()

    results = {b: {s: None for s in runner.solver_names} for b in runner.benchmarks}
    for r in runner.results:
        results[r.benchmark][r.solver] = r.time

    for mark in runner.benchmarks:
        print(mark)
        for solver_name in runner.solver_names:
            solver_time = (
                " -"
                if results[mark][solver_name] is None
                else f"{round(results[mark][solver_name] * 1000)}ms"
            )
            print(f"\t{solver_time.rjust(7)} - {solver_name}")
