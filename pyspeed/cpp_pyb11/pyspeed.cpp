#include "mergesort.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using std::u32string;

//std::vector<std::u32string> string_slice(py::list string_list, size_t start, size_t end){
std::vector<std::u32string> string_slice(const std::vector<std::u32string>& string_list, size_t start, size_t end){
    auto sliced = std::vector<std::u32string>();
    for(auto s : string_list){
//    for(py::handle i : string_list){
        try{
//            std::u32string s = i.cast<py::str>().cast<std::u32string>();
            if(start < s.size()){
                sliced.push_back(s.substr(start, end-start+1));
            }else{
                sliced.push_back(std::u32string());
            }
        }catch(py::cast_error &e){
            throw py::value_error("string_list may only contain strings!");
        }
    }
    return sliced;
}

std::u32string string_slice1(const py::str &input, size_t start, size_t end){
    try{
        std::u32string s = input.cast<std::u32string>();
        if(start < s.size()){
            return s.substr(start, end-start+1);
        }else{
            return std::u32string();
        }
    }catch(py::cast_error &e){
        throw py::value_error("string_list may only contain strings!");
    }
}

std::unordered_map<std::u32string, unsigned long> count_ngrams(const u32string& s, size_t ngram_n) {
    u32string padding = u32string(ngram_n - 1, U'$');
    u32string padded = padding + s + padding;
    auto counts = std::unordered_map<std::u32string, unsigned long>();
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

std::vector<std::unordered_map<std::u32string, unsigned long>> count_ngrams_list(
    const std::vector<std::u32string>& string_list, size_t ngram_n
) {
    auto resultlist = std::vector<std::unordered_map<std::u32string, unsigned long>>();
    for(const std::u32string& s : string_list){
        resultlist.push_back(count_ngrams(s, ngram_n));
    }
    return resultlist;
}

PYBIND11_MODULE(pyspeed_pyb11, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("mergesort", &mergesortcpp, "Mergesort in C++");
    m.def("string_slice", &string_slice, "string_slice in C++");
    m.def("string_slice1", &string_slice1, "string_slice in C++");
    m.def("count_ngrams", &count_ngrams, "count ngrams in C++");
    m.def("count_ngrams_list", &count_ngrams_list, "count ngrams in C++");
}

