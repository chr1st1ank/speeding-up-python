# python-metrics
Small benchmarks to compare different options to speed up Python code.

This small project should help to:
- provide an overview of practical options to speed up Python code
- shows what performance improvements can be expected by the different options for some common use cases
- gives an indication of the development overhead when using a certain framework instead of pure Python
- offers example code which can be transferred to other use cases

Note that it is not considered important whether pure Python code is used (as with numba or with leveraging specialized Python modules. Also using other languages with an easy binding to Python such as Julia or C++ are a feasible option for practical use cases.

The benchmarks can't tell if a certain language or framework is fast or slow. First only the combination with Python is tested and secondly the benchmarks are picked mostly for being easily implementable and for giving a feeling of how to use a certain framework from Python in different scenarios. And lastly also the environment where I run these things is not controlled. Results might look very different on a different machine or platform.

## Benchmarks used for comparison
### 1. Mergesort 
[Mergesort](https://en.wikipedia.org/wiki/Merge_sort) is a common and efficient array sorting algorithm. It is interesting for performance measurement, because it is a realistic type of algorithm with recursion, loops and if/else statements. But still it is easy enough to implement. The implementations used represent the
"Top-down implementation" sketched out on wikipedia.

### 2. Groupby-Sum
The task is to calculate sums per group key on tabular data. Input is a dictionary of columns, output is a dictionary of aggregates in columns.

### 3. String slice
Input is a list of unicode strings. Every string has to be sliced and the first n characters have to be returned. The difficulty lies in the proper handling of unicode characters. ASCII characters are heavily overrepresented in the test strings (like in many real applications), so that handling of utf-8 strings pays off compared to a dump wchar approach. 

## Comments on the frameworks / languages used

### 1. Pure Python
The implementation in pure Python serves as reference for all other solutions.

### 2. Numba
[Numba](http://numba.pydata.org/) is an open source JIT compiler that translates a subset of Python and NumPy code into fast machine code. It used the [LLVM JIT compiler](https://llvm.org/).

Prerequisites:
- Only numba has to be installed, afterwards pure Python functions can be compiled just-in-time with the @jit decorator

Notes:
- Individual methods of Python classes cannot be compiled with the fast "nopython" mode, but the very slow "object" mode has to be used.
- Entire Python classes could be compiled, but not if they inherit from a pure Python class which is not compiled with Numba


### 3. Cython
[Cython](https://cython.org/) is a Python module which allows to access C or C++ code in an uncomplicated manner. In addition it offers the option to write code in a Python dialect with optional fixed typing which can be compiled by a C compiler and therefore runs faster afterwards. This option is what is meant by "Cython" here. Using Cython for C++ access is covered separately.

Prerequisites:
- The Python module Cython has to be installed and the C/C++ compiler used to compile the other Python modules
  has to be available (gcc on Linux and Mac, on windows most likely the Microsoft compiler is necessary).
  See <https://cython.readthedocs.io/en/latest/src/quickstart/install.html> for details.

Notes:
- The functions to be compiled have to be in a separate file with *.pyx ending. Compilation can be done "on the fly"
  as done here (with "pyximport"), or it can be done once beforehand with setup.py.
      
      
### 4. C++ via Cython
C++ implementation which is compiled and called with Cython.

Prerequisites:
- The Python module Cython has to be installed and the C/C++ compiler used to compile the other Python modules
  has to be available (gcc on Linux and Mac, on windows most likely the Microsoft compiler is necessary).
  See <https://cython.readthedocs.io/en/latest/pymetrics/quickstart/install.html> for details.
- Run the build script in pymetrics/cpp/build.sh to compile the C++ code before running the program.

Notes:
- Using C++ needs some overhead before it works:
  - A pyx file has to be written to describe the Python view of the C++ function
  - A pxd file needs to be there to declare the C++ functions to be sued
  - The C++ code itself goes into header (.h or .hpp) files and source files (.cpp)
  - A setup.py is necessary to define the compilation steps
  - The compilation has to be carried out before running the Python program (done by the build_cpp.sh script).


### 5. Julia
Solver using the [Julia programming language](https://julialang.org/) which has a comfortable binding for Python.

Prerequisites:
- Install Julia itself and the python module PyJulia (with `pip install julia`)
- In the Python interpreter, run once:
```python
import julia
julia.install()
```

Notes:
- Julia has to be written in separate *.jl files, but they don't have to be compiled explicitly. Instead they are
  compiled just-in-time when the functions are executed for the first time.
- With the approach taken here (`julia.include(<filename>)`) only the last function of a *.jl file is imported.
  There is also an alternative `importall` method.
- The code assumes that the standard "high-level" mode of PyJulia can be used, which needs Julia to be on the PATH
  variable. Alternative approaches are described on the [PyJulia page](https://github.com/JuliaPy/pyjulia)
      
### 6. Rust
Implementation in the Rust programming language using the [Pyo3 bindings](https://pyo3.rs). It allows to compile native Python extensions with minimal overhead.

Prerequisites:
- Run `cargo init` on the repository root, add pyo3 as dependency in the Cargo.toml and define a library as build target.
- Run `cargo build --release` when the Rust code is finished
- Copy or link the .so file to the Python package (done by the build_rust.sh script).
      
## Latest results
Output of the last run on my laptop:

```
mergesort
	  236ms - Pure Python
	  285ms - Numba
	   90ms - Cythonized Python
	   57ms - Julia
	   17ms - C++
	   11ms - Rust from Python
groupby_sum
	  130ms - Pure Python
	      - - Numba
	   79ms - Cythonized Python
	      - - Julia
	      - - C++
	  100ms - Rust from Python
string_slice
	  196ms - Pure Python
	      - - Numba
	  150ms - Cythonized Python
	      - - Julia
	      - - C++
	  410ms - Rust from Python

System information:

Architecture: x86_64 / 64bit
System: Linux / 5.11.11-arch1-1
Python: CPython 3.9.2 built with ('glibc', '2.33')
Processors: 
    4 x  Intel(R) Core(TM) i5 CPU       M 520  @ 2.40GHz
```

## Contributing

If you are interested in contributing, feel free to contact me or to just write a pull request. I am particularly interested in:
- Further benchmarks and their implementation with the different frameworks
- Tips for the one or other additional framework. Precondition: It should be simple to set up and use and not add too many additional dependencies
- Hints on possible improvements for some of the implementations. The goal is to leverage the best implementation option for each respective language. The implementations should however all stick to the same benchmark definition. For example it would not be very enlightening to compare an implementation with memoization in one language to one without in another one.

