
from benchmark_runner import BenchmarkRunner
import benchmark
import python_solver
import numba_solver
import cython_solver
import julia_solver
import cpp_solver

import sys
import platform
from collections import Counter


def system_info():
    print("\nSystem information:\n")

    # Architecture
    print(f"Architecture: {platform.machine()} / {platform.architecture()[0]}")
    print(f"System: {platform.system()} / {platform.release()}")
    print(f"Python: {platform.python_implementation()} {platform.python_version()} built with {platform.libc_ver()}")

    print("Processors: ")  # TODO: Unix specific!
    try:
        with open("/proc/cpuinfo", "r")  as f:
            cpu_info = Counter([x.strip().split(":")[1] for x in f.readlines() if "model name" in x])
            for name, count in cpu_info.items():
                print(f"    {count} x {name}")
    except:
        print(platform.processor())  # May return empty string!


if __name__ == '__main__':
    runner = BenchmarkRunner(solvers=[
            python_solver.PythonSolver(),
            numba_solver.NumbaSolver(),
            cython_solver.CythonSolver(),
            julia_solver.JuliaSolver(),
            cpp_solver.CppSolver
        ],
        benchmarks=[
            benchmark.mergesort_benchmark
        ]
    )
    runner.time_it()
    runner.verify_results()

    results = {b: {s: None for s in runner.solver_names} for b in runner.benchmarks}
    for r in runner.results:
        results[r.benchmark][r.solver] = r.time

    for mark in runner.benchmarks:
        print(mark)
        for s in runner.solver_names:
            print(f"\t{round(results[mark][s]*1000)}ms - {s}")

    system_info()
