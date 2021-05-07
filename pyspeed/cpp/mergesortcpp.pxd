
from libcpp.vector cimport vector
ctypedef long long bigint

cdef extern from "mergesort.hpp":
    cdef vector[long long] mergesortcpp(vector[long long] l)
