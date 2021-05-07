"""C++ implementation which is compiled and called with Cython.

Prerequisites:
    * The Python module Cython has to be installed and the C/C++ compiler used to compile the other Python modules
      has to be available (gcc on Linux and Mac, on windows most likely the Microsoft compiler is necessary).
      See <https://cython.readthedocs.io/en/latest/pymetrics/quickstart/install.html> for details.
    * Run the build script in pymetrics/cpp/build.sh to compile the C++ code before running the program.

Notes:
    * Using C++ needs some overhead before it works:
      - A pyx file has to be written to describe the Python view of the C++ function
      - A pxd file needs to be there to declare the C++ functions to be sued
      - The C++ code itself goes into header (.h or .hpp) files and source files (.cpp)
      - A setup.py is necessary to define the compilation steps
      - The compilation has to be carried out before running the Python program

"""

# import pyximport; pyximport.install(language_level=3)
from cpp import mergesortcpp

from benchmark_solver import BenchmarkSolver
from typing import List

class CppSolver(BenchmarkSolver):
    @staticmethod
    def description():
        return "C++"

    @staticmethod
    def direct_dependencies():
        return ['Cython']

    @staticmethod
    def mergesort(l: List) -> List:
        return mergesortcpp.mergesort(l)
