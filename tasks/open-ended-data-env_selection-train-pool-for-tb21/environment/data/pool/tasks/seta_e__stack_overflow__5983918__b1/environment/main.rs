// mathutil — integer arithmetic utilities
//
// Copyright (c) 2024 Example Corp.
// All rights reserved.

use std::env;
use std::process;

#[inline(never)]
fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[inline(never)]
fn multiply(a: i32, b: i32) -> i32 {
    a * b
}

#[inline(never)]
fn compute(x: i32, y: i32) -> i32 {
    let sum = add(x, y);
    let product = multiply(x, y);
    sum + product
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <x> <y>", args[0]);
        process::exit(1);
    }
    let x: i32 = args[1].parse().expect("Invalid integer");
    let y: i32 = args[2].parse().expect("Invalid integer");
    let result = compute(x, y);
    println!("compute({}, {}) = {}", x, y, result);
}
