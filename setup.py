from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(['pyspeed/cpp/mergesortcpp.pyx'], language_level=3),
)
