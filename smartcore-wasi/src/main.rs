use chrono::Utc;
use smartcore_wasi_lib::{init, load_model};
use std::env::args;
use std::time::Instant;

fn main() {
    let mut path = String::from("iris_knn.model\0");
    let ptr = path.as_mut_ptr();
    std::mem::forget(ptr);
    #[cfg(target_arch = "x86_64")]
    init(ptr.cast::<i8>());
    #[cfg(all(target_arch = "aarch64", target_arch = "arm"))]
    init(ptr);
    let mut performances: Vec<u128> = Vec::new();
    let start_time = Utc::now();
    for _ in 0..1000 {
        let now = Instant::now();
        load_model();
        let diff = now.elapsed().as_nanos();
        performances.push(diff);
    }
    let end_time = Utc::now();
    let info = os_info::get();
    let arch = std::env::consts::ARCH;
    let os = std::env::consts::OS;
    let os_type = info.os_type();
    let os_version = info.version();
    let args: Vec<String> = args().collect();
    let mut output_file = String::from("data.csv");
    for arg in args {
        if arg.contains(".csv") {
            output_file = arg;
        }
    }
    let mut wtr = csv::WriterBuilder::new()
        .has_headers(true)
        .from_path(&output_file)
        .unwrap();
    wtr.write_record(&[
        "startTime",
        "endTime",
        "architecture",
        "os",
        "osType",
        "osVersion",
        "time(ns)",
    ])
    .unwrap();
    for perf in performances {
        wtr.write_record(&[
            start_time.to_string(),
            end_time.to_string(),
            arch.to_string(),
            os.to_string(),
            os_type.to_string(),
            os_version.to_string(),
            perf.to_string(),
        ])
        .unwrap();
    }
    wtr.flush().unwrap();
    println!("Written benchmark data to {}", output_file);
}
