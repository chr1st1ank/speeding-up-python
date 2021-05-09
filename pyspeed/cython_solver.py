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

import pandas as pd

from benchmark_solver import BenchmarkSolver
from typing import List

class CythonSolver(BenchmarkSolver):
    def description(cls):
        return "Cythonized Python"

    def mergesort(self, l: List) -> List:
        return cython_backend.mergesort_cy(l)

    def groupby_sum(self, data):
        return cython_backend.groupby_sum_cy(data)

    def string_slice(self, test_data):
        string_list: List[str] = test_data["strings"]
        start: int = test_data["start"]
        end: int = test_data["end"]
        return cython_backend.string_slice(string_list, start, end)

    def ngram_count(self, test_data):
        string_list: List[str] = test_data["strings"]
        ngram_n: int = test_data["ngram_n"]
        return cython_backend.count_ngrams_in_list(string_list, ngram_n)
