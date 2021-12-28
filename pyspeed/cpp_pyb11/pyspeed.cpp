#include "mergesort.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "extern/smhasher/MurmurHash3.h"

namespace py = pybind11;
using std::u32string;

//std::vector<u32string> string_slice(py::list string_list, size_t start, size_t end){
std::vector<u32string> string_slice(const std::vector<u32string>& string_list, size_t start, size_t end){
    auto sliced = std::vector<u32string>();
    for(auto s : string_list){
//    for(py::handle i : string_list){
        try{
//            u32string s = i.cast<py::str>().cast<u32string>();
            if(start < s.size()){
                sliced.push_back(s.substr(start, end-start+1));
            }else{
                sliced.push_back(u32string());
            }
        }catch(py::cast_error &e){
            throw py::value_error("string_list may only contain strings!");
        }
    }
    return sliced;
}

u32string string_slice1(const py::str &input, size_t start, size_t end){
    try{
        u32string s = input.cast<u32string>();
        if(start < s.size()){
            return s.substr(start, end-start+1);
        }else{
            return u32string();
        }
    }catch(py::cast_error &e){
        throw py::value_error("string_list may only contain strings!");
    }
}

std::unordered_map<u32string, unsigned long> count_ngrams(const u32string& s, size_t ngram_n) {
    u32string padding = u32string(ngram_n - 1, U'$');
    u32string padded = padding + s + padding;
    auto counts = std::unordered_map<u32string, unsigned long>();
    for(size_t i=0; i<=padded.size()-ngram_n; ++i){
        u32string ngram = padded.substr(i, ngram_n);
        if(counts.contains(ngram)){
            counts[ngram] = counts[ngram] + 1;
        }else{
            counts[ngram] = 1;
        }
    }
    return counts;
}

std::vector<std::unordered_map<u32string, unsigned long>> count_ngrams_list(
    const std::vector<u32string>& string_list, size_t ngram_n
) {
    auto resultlist = std::vector<std::unordered_map<u32string, unsigned long>>();
    for(const u32string& s : string_list){
        resultlist.push_back(count_ngrams(s, ngram_n));
    }
    return resultlist;
}


const uint32_t MERSENNE_PRIME = 4294967295UL;	// mersenne prime (1 << 32) - 1

uint32_t murmur3(const std::string& s){
    uint32_t out = 0L;
    MurmurHash3_x86_32(s.c_str(), s.size(), 0, &out);
    return out;
}

std::vector<uint32_t> calc_minhashes(
    const std::vector<std::string>& shingle_list, py::array_t<uint32_t> A, py::array_t<uint32_t> B
) {
    auto crchashes = std::vector<uint32_t>();
    for(const std::string& s : shingle_list){
        crchashes.push_back(murmur3(s));
    }
    auto hashes_permuted = std::vector<uint32_t>();
    if( A.shape(0) != B.shape(0)){
        throw std::invalid_argument("Shapes don't match");
    }

    auto a_access = A.unchecked<1>(); // Will throw if ndim != 1
    auto b_access = B.unchecked<1>(); // Will throw if ndim != 1
    for (py::ssize_t i = 0; i < a_access.shape(0); ++i){
        uint32_t minhash = MERSENNE_PRIME;
        for(uint32_t crchash : crchashes){
            uint32_t h = (a_access(i) * crchash + b_access(i)) % MERSENNE_PRIME;
            if (h < minhash){
                minhash = h;
            }
        }
        hashes_permuted.push_back(minhash);
    }
    return hashes_permuted;
}

PYBIND11_MODULE(pyspeed_pyb11, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("mergesort", &mergesortcpp, "Mergesort in C++");
    m.def("string_slice", &string_slice, "string_slice in C++");
    m.def("string_slice1", &string_slice1, "string_slice in C++");
    m.def("count_ngrams", &count_ngrams, "count ngrams in C++");
    m.def("count_ngrams_list", &count_ngrams_list, "count ngrams in C++");
    m.def("calc_minhashes", &calc_minhashes, "calculate minhashes for a list of shingles C++");
    m.def("murmur3", &murmur3, "murmur3 hash of a string in C++");
}

