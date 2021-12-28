from distutils.core import setup
from glob import glob
from pybind11.setup_helpers import Pybind11Extension

setup(
    ext_modules=[
        Pybind11Extension(
            "pyspeed_pyb11",
            sorted(glob("*.cpp")) + ["extern/smhasher/MurmurHash3.cpp"],  # Sort source files for reproducibility
            cxx_std=20
        ),
    ],
)
