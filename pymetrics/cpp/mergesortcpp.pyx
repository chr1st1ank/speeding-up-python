# distutils: language = c++
# distutils: sources = mergesort.cpp

from mergesortcpp cimport mergesortcpp
from typing import List

def mergesort(lst: List) -> List:
  return mergesortcpp(lst)
