use std::ffi::{CStr};
use std::fs;
use std::io::{Read, Write};
use std::mem;
use std::os::raw::{c_char, c_void};

#[no_mangle]
pub extern "C" fn allocate(size: usize) -> *mut c_void {
    let mut buffer = Vec::with_capacity(size);
    let pointer = buffer.as_mut_ptr();
    mem::forget(buffer);

    pointer as *mut c_void
}

#[no_mangle]
pub extern "C" fn deallocate(pointer: *mut c_void, capacity: usize) {
    unsafe {
        let _ = Vec::from_raw_parts(pointer, 0, capacity);
    }
}

fn process(input_fname: &str, output_fname: &str) -> Result<(), String> {
    let mut input_file = fs::File::open(input_fname)
        .map_err(|err| format!("error opening input {}: {}", input_fname, err))?;
    let mut contents = Vec::new();
    input_file
        .read_to_end(&mut contents)
        .map_err(|err| format!("read error: {}", err))?;

    let mut output_file = fs::File::create(output_fname)
        .map_err(|err| format!("error opening output {}: {}", output_fname, err))?;
    output_file
        .write_all(&contents)
        .map_err(|err| format!("write error: {}", err))
}

#[no_mangle]
pub unsafe fn load_model(input_ptr: *mut c_char, output_ptr: *mut c_char) -> () {
    let input_fname = CStr::from_ptr(input_ptr);
    let output_fname = CStr::from_ptr(output_ptr);

    if let Err(err) = process(
        input_fname.to_str().unwrap(),
        output_fname.to_str().unwrap(),
    ) {
        eprintln!("{}", err)
    }
}
