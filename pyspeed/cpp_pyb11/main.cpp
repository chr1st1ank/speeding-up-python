#include "mergesort.hpp"

#include <iostream>
#include <random>

using namespace std;

typedef vector<long long> NumberVector;

void print_vector(const NumberVector& vec){
    cout << "[" << endl;
    for(auto it=vec.begin(); it!=vec.end(); ++it){
        cout << "\t" << *it << "," << endl;;
    }
    cout << "]" << endl;
}

void run_mergesort() {
    NumberVector unsorted = NumberVector();
    default_random_engine generator(123);
    while (unsorted.size() < 20) {
        unsorted.push_back(generator());
    }
    print_vector(unsorted);

    auto sorted = mergesortcpp(unsorted);
    print_vector(sorted);
}

int main()
{
    run_mergesort();
    return 0;
}
