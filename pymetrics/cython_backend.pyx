"""Cython code which is compiled and used from Python."""

def merge_cy(l, r):
    """Returns a sorted list with all elements from l and r"""
    result = []

    while len(l) and len(r):
        if l[0] <= r[0]:
            result.append(l.pop(0))
        else:
            result.append(r.pop(0))
    if l:
        return result + l
    if r:
        return result + r

    return result


def mergesort_cy(l):
    cdef int x = len(l)
    if x <= 1:
        return l
    x /= 2
    left = mergesort_cy(l[:x])
    right = mergesort_cy(l[x:])
    return merge_cy(left, right)
