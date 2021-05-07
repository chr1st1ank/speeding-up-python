use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
// use pyo3::types::PyList;


// vector<long long> merge(vector<long long> left, vector<long long> right)
// {
//     vector<long long> ret;
//     auto l_it = left.begin();
//     auto r_it = right.begin();
//     while(l_it != left.end() && r_it != right.end())
//     {
//         if(*l_it <= *r_it)
//             ret.push_back(*l_it++);
//         else
//             ret.push_back(*r_it++);
//     }
//     while(l_it != left.end())
//     {
//         ret.push_back(*l_it++);
//     }
//     while(r_it != right.end())
//     {
//         ret.push_back(*r_it++);
//     }
//     return ret;
// }
fn merge(left: &[i64], right: &[i64]) -> Vec<i64> {
    let mut ret: Vec<i64> = Vec::new();
    let mut l_it = left.iter();
    let mut r_it = right.iter();
    let mut l_next = l_it.next();
    let mut r_next = r_it.next();
    loop {
        if let Some(l_val) = l_next {
            if let Some(r_val) = r_next {
                if l_val <= r_val {
                    ret.push(*l_val);
                    l_next = l_it.next();
                } else {
                    ret.push(*r_val);
                    r_next = r_it.next();
                }
            } else {
                break;
            }
        } else {
            break;
        }
    }
    while let Some(v) = l_next {
        ret.push(*v);
        l_next = l_it.next();
    }
    while let Some(v) = r_next {
        ret.push(*v);
        r_next = r_it.next();
    }
    return ret;
}

fn mergesort_rs(l: &[i64]) -> Vec<i64> {
    if l.len() <= 1 {
        return l.to_vec();
    }
    let (left, right) = l.split_at(l.len() / 2);
    let left = mergesort_rs(left);
    let right = mergesort_rs(right);
    return merge(&left, &right);
}

#[pyfunction]
fn mergesort(l: Vec<i64>) -> PyResult<Vec<i64>> {
    Ok(mergesort_rs(&l))
}


/// Formats the sum of two numbers as string.
#[pyfunction]
pub fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}


/// Formats the sum of a list of numbers as string.
#[pyfunction]
// pub fn sum_of_list(l:&PyList) -> PyResult<String> {
pub fn sum_of_list(l: Vec<i64>) -> PyResult<String> {
    let mut sum: i64 = 0;
    for x in l {
        sum += x;
    }
    Ok(sum.to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn pyspeed_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(mergesort, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(sum_of_list, m)?)?;

    Ok(())
}
