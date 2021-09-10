"""C++ implementation which is compiled and linked with pybind11.

Prerequisites:
    * The Python module pybind11 has to be installed and the C/C++ compiler used to compile the other Python modules
      has to be available (gcc on Linux and Mac, on windows most likely the Microsoft compiler is necessary).
      See <https://cython.readthedocs.io/en/latest/pymetrics/quickstart/install.html> for details.
    * Run the build script build_cpp.sh to compile the C++ code before running the program.

Notes:
    * Using C++ needs some overhead before it works:
      - The C++ code itself goes into header (.h or .hpp) files and source files (.cpp)
      - A setup.py is necessary to define the compilation steps
      - The compilation has to be carried out before running the Python program

"""
from . import cpp_pyb11 as cpp

from .benchmark_solver import BenchmarkSolver
from typing import List, Dict


class CppPyb11Solver(BenchmarkSolver):
    def description(self):
        return "C++ (pybind11)"

    def string_slice(self, test_data: Dict):
        string_list: List[str] = test_data["strings"]
        start: int = test_data["start"]
        end: int = test_data["end"]
        return cpp.string_slice(string_list, start, end)

    def mergesort(self, l: List) -> List:
        return cpp.mergesort(l)

    def ngram_count(self, test_data):
        string_list: List[str] = test_data["strings"]
        ngram_n: int = test_data["ngram_n"]
        return cpp.count_ngrams_list(string_list, ngram_n)
        # return [
        #     cpp.count_ngrams(s, ngram_n) for s in string_list
        # ]
