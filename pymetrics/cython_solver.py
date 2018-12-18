"""Cython implementation which uses almost exactly the Python implementation but is compiled with Cython.

Prerequisites:
    * The Python module Cython has to be installed and the C/C++ compiler used to compile the other Python modules
      has to be available (gcc on Linux and Mac, on windows most likely the Microsoft compiler is necessary).
      See <https://cython.readthedocs.io/en/latest/pymetrics/quickstart/install.html> for details.

Notes:
    * The functions to be compiled have to be in a separate file with *.pyx ending. Compilation can be done "on the fly"
      as done here (with "pyximport"), or it can be done once beforehand with setup.py.
"""

import pyximport; pyximport.install(language_level=3)
import cython_backend

from benchmark_solver import BenchmarkSolver
from typing import List

class CythonSolver(BenchmarkSolver):
    def description(cls):
        return "Cythonized Python"

    def direct_dependencies(cls):
        return ['cython']

    def mergesort(self, l: List) -> List:
        return cython_backend.mergesort_cy(l)

