use rayon::prelude::*;
use std::os::raw::{c_int, c_longlong};

extern "C" {
    fn compute_checksum(arr: *const c_int, n: c_int) -> c_longlong;
}

fn main() {
    let n: usize = 1000;
    let data: Vec<i32> = (0..n)
        .into_par_iter()
        .map(|i| (i + 1) as i32)
        .collect();

    let num_threads = rayon::current_num_threads();
    println!("Running with {} thread(s)", num_threads);

    let result = unsafe { compute_checksum(data.as_ptr(), n as c_int) };
    println!("Checksum: {}", result);
}
