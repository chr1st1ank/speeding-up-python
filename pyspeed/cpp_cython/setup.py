import pathlib
import shutil
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(['mergesortcpp.pyx'], language_level=3)
)
for f in pathlib.Path('./pyspeed/cpp_cython/').glob('*.so'):
    shutil.copy(f, './')
