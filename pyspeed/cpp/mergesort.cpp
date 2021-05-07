
#include <vector>
#include <algorithm>
#include <iterator>
#include "mergesort.hpp"

using namespace std;

//template<class InputIt, class OutputIt>
//void merge(InputIt l_it, InputIt l_end,
//            InputIt r_it, InputIt r_end,
//            OutputIt o_it)
//{
//    while(l_it!=l_end && r_it!=r_end)
//    {
//        if(*l_it <= *r_it)
//        {
//            *o_it++ = *l_it++;
//        }else{
//            *o_it++ = *r_it++;
//        }
//    }
//    if(l_it!=l_end)
//    {
//        copy(l_it, l_end, o_it);
//        return;
//    }
//    if(r_it!=r_end)
//    {
//        copy(r_it, r_end, o_it);
//        return;
//    }
//}
//
//template<class RAIterator, class OutputIt>
//void mergesort(RAIterator l_it, RAIterator l_end, OutputIt o_it)
//{
//    size_t s = std::distance(l_it, l_end);
//    if(s <= 1)
//    {
//        copy(l_it, l_end, o_it);
//        return;
//    }
//    auto middle = (s/2);
//    mergesort(l_it, l_it+middle, o_it);
//    mergesort(l_it+middle, l_end, o_it+middle);
//    merge(l_it, l_it+middle, l_it+middle, l_end,  o_it);
//}
//
//template<class T>
//vector<T> mergesort(vector<T>& l)
//{
//    vector<T> working_copy(l.size());
//    mergesort(l.begin(), l.end(), working_copy.begin());
//    return working_copy;
//}

vector<long long> merge(vector<long long> left, vector<long long> right)
{
    vector<long long> ret;
    auto l_it = left.begin();
    auto r_it = right.begin();
    while(l_it != left.end() && r_it != right.end())
    {
        if(*l_it <= *r_it)
            ret.push_back(*l_it++);
        else
            ret.push_back(*r_it++);
    }
    while(l_it != left.end())
    {
        ret.push_back(*l_it++);
    }
    while(r_it != right.end())
    {
        ret.push_back(*r_it++);
    }
    return ret;
}

vector<long long> mergesortcpp(vector<long long> l)
{
    if(l.size() <= 1)
        return l;
    auto middle = (l.size()/2);
    vector<long long> left(l.begin(), l.begin()+middle);
    vector<long long> right(l.begin()+middle, l.end());
    left = mergesortcpp(left);
    right = mergesortcpp(right);
    return merge(left, right);
}
