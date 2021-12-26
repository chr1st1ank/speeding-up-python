use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::types::PyList;
use pyo3::wrap_pyfunction;
use rayon::prelude::*;
use std::collections::HashMap;
// use substring::Substring;
// use unicode_segmentation::UnicodeSegmentation;

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
        None => {
            return Err(pyo3::exceptions::PyValueError::new_err("keys missing"));
        }
    };
    // let keys = keys.downcast::<PyList>()?;
    let keys: Vec<i64> = keys.extract()?;
    let mut groups: Vec<i64> = keys.clone();
    groups.sort();
    groups.dedup();

    // let result_dict = PyDict::new(py);
    let mut result_dict: HashMap<String, PyObject> = HashMap::new();

    for (column, values) in data_table.iter() {
        let column: String = column.extract()?;
        if column == "keys" {
            continue;
        }
        if let Ok(values) = values.extract::<Vec<i64>>() {
            let sum_vec: Vec<i64> = sum_by_group(&keys, &values, &groups);
            result_dict.insert(column, sum_vec.into_py(py));
        } else if let Ok(values) = values.extract::<Vec<f64>>() {
            let sum_vec: Vec<f64> = sum_by_group(&keys, &values, &groups);
            result_dict.insert(column, sum_vec.into_py(py));
        }
    }
    result_dict.insert("keys".to_string(), groups.into_py(py));

    Ok(result_dict.into_py(py))
}

fn sum_by_group<T>(keys: &[i64], values: &[T], groups: &[i64]) -> Vec<T>
where
    T: std::ops::AddAssign<T> + Copy + Default,
{
    let mut sums: HashMap<i64, T> = HashMap::new();

    for (i, v) in values.iter().enumerate() {
        if let Some(key) = keys.get(i) {
            *(sums.entry(*key).or_default()) += *v;
        }
    }
    let mut sum_vec: Vec<T> = Vec::new();
    for k in groups {
        if let Some(sum) = sums.get(k) {
            sum_vec.push(*sum);
        }
    }
    sum_vec
}

#[pyfunction]
// fn string_slice(strings: Vec<&str>, start: usize, end: usize) -> PyResult<Vec<&str>> {
fn string_slice(strings: Vec<&str>, start: usize, end: usize) -> PyResult<Vec<String>> {
    let new_strings = strings
        .iter()
        .map(|s: &&str| s.chars().skip(start).take(end - start + 1).collect())
        .collect();
    Ok(new_strings)
}

fn pad_both_sides(s: &str, pad_char: char, times: usize) -> String {
    let mut padded = String::with_capacity(s.len() + 2 * times);
    for _ in 0..(times) {
        padded.push(pad_char)
    }
    padded.push_str(s);
    for _ in 0..(times) {
        padded.push(pad_char)
    }
    padded
}

fn count_ngrams_rs(s: &str, ngram_n: usize) -> HashMap<String, u32> {
    // Padding. Examle for ngram_n = 3: "abc" => "$$abc$$"
    let padded = pad_both_sides(s, '$', ngram_n - 1);

    let mut counts: HashMap<String, u32> = HashMap::new();
    // counts.insert(String::from("x"), 1);
    // let mut iter = padded.graphemes(true);
    let mut iter = padded.chars();
    loop {
        // let ngram = iter.as_str().substring(0, ngram_n).to_string();
        let ngram = iter.clone().take(ngram_n).collect::<String>();
        if ngram.len() < ngram_n {
            break;
        }
        *counts.entry(ngram).or_insert(0) += 1;
        iter.next();
    }

    counts
}

#[pyfunction]
fn count_ngrams(py: Python, s: &str, ngram_n: usize) -> PyResult<PyObject> {
    Ok(count_ngrams_rs(s, ngram_n).into_py(py))
}

#[pyfunction]
fn count_ngrams_list_rs(strings: Vec<&str>, ngram_n: usize) -> Vec<HashMap<String, u32>> {
    let results: Vec<HashMap<String, u32>> = strings
        .iter()
        .map(|s| count_ngrams_rs(s, ngram_n))
        .collect();
    results
}

#[pyfunction]
fn count_ngrams_list(py: Python, strings: Vec<&str>, ngram_n: usize) -> PyResult<PyObject> {
    let results: Vec<HashMap<String, u32>> = count_ngrams_list_rs(strings, ngram_n);
    // let results: Vec<HashMap<String, u32>> = strings
    //     .iter()
    //     .map(|s| count_ngrams_rs(s, ngram_n))
    //     .collect();
    Ok(results.into_py(py))
}

#[pyfunction]
fn count_ngrams_list_native(py: Python, strings: &PyList, ngram_n: usize) -> PyResult<PyObject> {
    let results: Vec<HashMap<String, u32>> = strings.iter()
        .map(|s| -> String {s.extract().unwrap()})
        .map(|s| count_ngrams_rs(&s, ngram_n))
        .collect();
    Ok(results.into_py(py))
}

#[pyfunction]
fn count_ngrams_list_parallel(
    py: Python,
    strings: Vec<&str>,
    ngram_n: usize,
) -> PyResult<PyObject> {
    let results: Vec<HashMap<String, u32>> = strings
        .into_par_iter()
        .map(|s| count_ngrams_rs(s, ngram_n))
        .collect();

    Ok(results.into_py(py))
}

#[pyfunction]
fn strlen(s: &str) -> PyResult<usize> {
    Ok(s.chars().count())
}

#[pymodule]
fn pyspeed_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(mergesort, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(sum_of_list, m)?)?;
    m.add_function(wrap_pyfunction!(groupby_sum, m)?)?;
    m.add_function(wrap_pyfunction!(string_slice, m)?)?;
    m.add_function(wrap_pyfunction!(count_ngrams, m)?)?;
    m.add_function(wrap_pyfunction!(count_ngrams_list, m)?)?;
    m.add_function(wrap_pyfunction!(count_ngrams_list_native, m)?)?;
    m.add_function(wrap_pyfunction!(count_ngrams_list_parallel, m)?)?;
    m.add_function(wrap_pyfunction!(strlen, m)?)?;

    Ok(())
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!("$$abc$$", pad_both_sides("abc", '$', 2));
    }
}

