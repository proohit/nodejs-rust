use chrono::Utc;
use smartcore_wasi_lib::{init, load_model};
use std::env;
use std::io::Write;
use std::time::Instant;

fn main() {
    let mut path = String::from("iris_knn.model\0");
    let ptr = path.as_mut_ptr();
    std::mem::forget(ptr);
    #[cfg(target_arch = "x86_64")]
    init(ptr.cast::<i8>());
    #[cfg(not(target_arch = "x86_64"))]
    init(ptr);
    let mut performances: Vec<u128> = Vec::new();
    let start_time = Utc::now();
    let num_executions: i32 = env::var("noe").unwrap_or(1000.to_string()).parse().unwrap();
    println!("Executing {} times", num_executions);
    for _ in 0..num_executions {
        let now = Instant::now();
        load_model();
        let diff = now.elapsed().as_nanos();
        performances.push(diff);
    }
    let end_time = Utc::now();

    let output = format!(
        "startTime:{}\nendTime:{}\ndata: {:?}",
        start_time, end_time, &performances
    );
    let mut file = std::fs::File::create("data-native.csv").unwrap();
    file.write_all(output.as_bytes()).unwrap();
}
