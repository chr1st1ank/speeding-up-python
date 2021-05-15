import timeit
from datasketch.minhash import MinHash
from datasketch.weighted_minhash import WeightedMinHashGenerator
from datasketch.lsh import MinHashLSH

from benchmark import lsh_benchmark

b = lsh_benchmark()
# print(len(b.data["strings"]))
# exit(0)
permutations = 100

start = timeit.default_timer()
lsh = MinHashLSH(threshold=0.25, num_perm=permutations)
strings = []
hashes = []
for i, s in enumerate(b.data["strings"]):
    # strings.append(' '.join(s))
    mg = MinHash(permutations)
    mg.update_batch(w.encode('utf-8') for w in s)
    # print(s, mg)
    # hashes.append(mg)
    lsh.insert(i, mg, check_duplication = False)
print("Indexing", timeit.default_timer() - start)
start = timeit.default_timer()

count_matches = 0
for i in range(len(strings)):
    matches = lsh.query(hashes[i])
    if set(matches) != {i}:
        count_matches += len(matches) -1
        # print(strings[i], "=>", ', '.join([
        #     f'"{strings[k]}"' for k in matches if k != i
        # ]))
print("Lookup", timeit.default_timer() - start)



#     lsh.insert("m", m)
#
# for s in b.data["strings"]:
#     result = lsh.query(s)
#     print(s, result)
#     break
#     # print("Estimated Jaccard m1, m2", m1.jaccard(m2))

##############################################
# import random
# import cProfile
# import timeit
#
# import rust_solver
# from benchmark import ngram_count_benchmark
#
# # print(string_slice_benchmark)
# random.seed(123)
#
# # Set up some benchmark function
# rusts = rust_solver.RustSolver()
# testdata = ngram_count_benchmark().data
# def bench():
#     rusts.ngram_count(testdata)
#
# # Profile and time it
# # cProfile.run('bench()', sort='tottime')
# cProfile.run('bench()', sort='cumtime')
# timer = timeit.Timer('bench()', globals=dict(bench=bench))
# timed = min(timer.repeat(repeat=5, number=3))/3*1000
# print(f"Timeit: {timed:.2f}ms" )




##############################################
# print(rusts.ngram_count(testdata))


# for s in ["abc", "äöü", "áôü", "奥会多"]:
#     print(len(s), pyspeed_rust.strlen(s))
# data_table = {
#     "keys": [-5, 10, 4, -5],
#     "v1": [1, 2, 3, 4],
#     "v2": [-1, -2, -3, -4],
# }
# print(pyspeed_rust.count_ngrams("abcabc", 3))
# print(pyspeed_rust.sum_as_string(2, 22))
# print(pyspeed_rust.sum_of_list([random.randint(-100, 100) for _ in range(1000)]))
# print(pyspeed_rust.mergesort([1,5,8,1,9]))

# from python_solver import PythonSolver
# from cython_solver import CythonSolver
# from benchmark import mergesort_benchmark, groupby_sum_benchmark
#
# result = PythonSolver().groupby_sum(groupby_sum_benchmark.data)
# for k in result.keys():
#     print (k, result[k])
#
#
# result = CythonSolver().groupby_sum(groupby_sum_benchmark.data)
# for k in result.keys():
#     print (k, result[k])