# distutils: language = c++
# distutils: sources = pymetrics/cpp/mergesort.cpp

from . cimport mergesortcpp
from typing import List

def mergesort(lst: List) -> List:
  return mergesortcpp(lst)
