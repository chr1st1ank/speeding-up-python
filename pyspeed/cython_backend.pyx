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


def groupby_sum_cy(data_dict):
    sorted_keys = sorted(set(data_dict["keys"]))
    output = {
        "keys": sorted_keys
    }
    columns = [c for c in data_dict.keys() if c != "keys"]
    for column in columns:
        output[column] = {k: 0 for k in sorted_keys}
        for k, v in zip(data_dict["keys"], data_dict[column]):
            output[column][k] += v
        output[column] = [output[column][k] for k in sorted_keys]
    return output


def string_slice(string_list, start: int, end: int):
    return [s[start:end+1] for s in string_list]
