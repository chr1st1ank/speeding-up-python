use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::PyDict;
use std::collections::HashMap;

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
pub fn sum_of_list(l: Vec<i64>) -> PyResult<String> {
    let mut sum: i64 = 0;
    for x in l {
        sum += x;
    }
    Ok(sum.to_string())
}

#[pyfunction]
pub fn groupby_sum(py: Python, data_table: &PyDict) -> PyResult<PyObject> {
    let keys = match data_table.get_item("keys") {
        Some(l) => l,
        None => { return Err(pyo3::exceptions::PyValueError::new_err("keys missing")); }
    };
    // let keys = keys.downcast::<PyList>()?;
    let keys: Vec<i64> = keys.extract()?;
    let mut groups: Vec<i64> = keys.clone();
    groups.sort();
    groups.dedup();

    // let result_dict = PyDict::new(py);
    let mut result_dict : HashMap<String, Vec<i64>> = HashMap::new();

    for (column, values) in data_table.iter() {
        let column: String = column.extract()?;
        if column == "keys" {
            continue;
        }
        let mut sums = HashMap::new();
        let values: Vec<i64> = values.extract()?;
        for i in 0..values.len() {
            if let Some(key) = keys.get(i) {
                let s = if let Some(old_sum) = sums.get(key) {
                    values[i] + old_sum
                }else{
                    values[i]
                };
                sums.insert(key, s);
            }
        }
        let mut sum_vec: Vec<i64> = Vec::new();
        for k in &groups {
            if let Some(sum) = sums.get(k) {
                sum_vec.push(*sum);
            }
        }
        result_dict.insert(column, sum_vec);
    }
    result_dict.insert("keys".to_string(), groups);

    Ok(result_dict.into_py(py))
}

#[pymodule]
fn pyspeed_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(mergesort, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(sum_of_list, m)?)?;
    m.add_function(wrap_pyfunction!(groupby_sum, m)?)?;

    Ok(())
}
