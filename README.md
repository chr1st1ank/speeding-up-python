# python-metrics
Small benchmarks to compare different options to speed up Python code.

This small project should help to:
- provide an overview of practical options to speed up Python code
- shows what performance improvements can be expected by the different options for some common use cases
- gives an indication of the development overhead when using a certain framework instead of pure Python
- offers example code which can be transferred to other use cases

Note that it is not considered important whether pure Python code is used (as with numba or with leveraging specialized Python modules. Also using other languages with an easy binding to Python such as Julia or C++ are a feasible option for practical use cases.


## Benchmarks used for comparison
**1. Mergesort** 
[Mergesort](https://en.wikipedia.org/wiki/Merge_sort) is a common and efficient array sorting algorithm. It is interesting for performance measurement, because it is a realistic type of algorithm with recursion, loops and if/else statements. But still it is easy enough to implement. The implementations used represent the
"Top-down implementation" sketched out on wikipedia.


## Comments on the frameworks / languages used

**1. Pure Python**

**2. Numba**
[Numba](http://numba.pydata.org/) is an open source JIT compiler that translates a subset of Python and NumPy code into fast machine code. It used the [LLVM JIT compiler](https://llvm.org/).

Prerequisites:
- Only numba has to be installed, afterwards pure Python functions can be compiled just-in-time with the @jit decorator

Notes:
- Individual methods of Python classes cannot be compiled with the fast "nopython" mode, but the very slow "object" mode has to be used.
- Entire Python classes could be compiled, but not if they inherit from a pure Python class which is not compiled with Numba

**3. Cython**
[Cython](https://cython.org/) is a Python module which allows to access C or C++ code in an uncomplicated manner. In addition it offers the option to write code in a Python dialect with optional fixed typing which can be compiled by a C compiler and therefore runs faster afterwards. This option is what is meant by "Cython" here. Using Cython for C++ access is covered separately.

Prerequisites:
    * The Python module Cython has to be installed and the C/C++ compiler used to compile the other Python modules
      has to be available (gcc on Linux and Mac, on windows most likely the Microsoft compiler is necessary).
      See <https://cython.readthedocs.io/en/latest/src/quickstart/install.html> for details.

Notes:
    * The functions to be compiled have to be in a separate file with *.pyx ending. Compilation can be done "on the fly"
      as done here (with "pyximport"), or it can be done once beforehand with setup.py.
      
**4. C++ via Cython**


**5. Julia**
Solver using the [Julia programming language](https://julialang.org/) which has a comfortable binding for Python.

Prerequisites:
    * Install Julia itself and the python module PyJulia (with `pip install julia`)

Notes:
    * Julia has to be written in separate *.jl files, but they don't have to be compiled explicitly. Instead they are
      compile just-in-time when the functions are executed for the first time.
    * With the approach taken here (`julia.include(<filename>)`) only the last function of a *.jl file is imported.
      There is also an alternative `importall` method.
    * The code assumes that the standard "high-level" mode of PyJulia can be used, which needs Julia to be on the PATH
      variable. Alternative approaches are described on the [PyJulia page](https://github.com/JuliaPy/pyjulia)
      
      
## Contributing

If you are interested in contributing, feel free to contact me or to just write a pull request. I am particularly interested in:
- Further benchmarks and their implementation with the different frameworks
- Tips for the one or other additional framework. Precondition: It should be simple to set up and use and not add too many additional dependencies
- Hints on possible improvements for some of the implementations. The goal is to leverage the best implementation option for each respective language. The implementations should however all stick to the same benchmark definition. For example it would not be very enlightening to compare an implementation with memoization in one language to one without in another one.

