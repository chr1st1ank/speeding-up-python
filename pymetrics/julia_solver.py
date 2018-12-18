"""Solver using the [Julia programming language](https://julialang.org/) which has a comfortable binding for Python.

Prerequisites:
    * Install Julia itself and the python module PyJulia (with `pip install julia`)

Notes:
    * Julia has to be written in separate *.jl files, but they don't have to be compiled explicitly. Instead they are
      compile just-in-time when the functions are executed for the first time.
    * With the approach taken here (`julia.include(<filename>)`) only the last function of a *.jl file is imported.
      There is also an alternative `importall` method.
    * The code assumes that the standard "high-level" mode of PyJulia can be used, which needs Julia to be on the PATH
      variable. Alternative approaches are described on the [PyJulia page](https://github.com/JuliaPy/pyjulia)
    * Julia seems to return numpy array instead of lists. This has to be taken care of.
"""

from typing import List
from benchmark_solver import BenchmarkSolver

import os
import julia

class JuliaSolver(BenchmarkSolver):
    def __init__(self):
        self.julia = julia.Julia()
        directory = os.path.realpath(os.path.dirname(__file__))
        print(directory)
        self.mergesort_jl = self.julia.include(os.path.join(directory, "julia/mergesort.jl"))

    def description(cls):
        return "Julia"

    def direct_dependencies(cls):
        return ["julia"]

    def mergesort(self, l: List) -> List:
        return list(self.mergesort_jl(l))

