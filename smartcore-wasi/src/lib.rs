#![feature(once_cell)]
use core::lazy::OnceCell;
use std::ffi::{CStr, CString};
use std::fs::File;
use std::io::Read;
use std::mem;
use std::os::raw::{c_char, c_void};
// DenseMatrix wrapper around Vec
use smartcore::linalg::naive::dense_matrix::DenseMatrix;
// Linear Regression
use smartcore::linear::linear_regression::LinearRegression;

static mut MODEL: OnceCell<LinearRegression<f64, DenseMatrix<f64>>> = OnceCell::new();

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

#[no_mangle]
pub fn init(model_path: *mut c_char) {
    unsafe {
        let file_name = CStr::from_ptr(model_path).to_str().unwrap();
        MODEL.get_or_init(|| {
            let mut buf: Vec<u8> = Vec::new();
            File::open(&file_name)
                .and_then(|mut f| f.read_to_end(&mut buf))
                .expect("Can not load model");
            bincode::deserialize(&buf).expect("Can not deserialize the model")
        });
    }
}

#[no_mangle]
pub fn load_model() -> *mut c_char {
    let data = DenseMatrix::from_array(1, 6, &[234.289, 235.6, 159.0, 107.608, 1947., 60.323]);
    let prediction = unsafe { MODEL.get().unwrap().predict(&data).unwrap() };
    let pred: String = prediction[0].to_string();
    return unsafe { CString::from_vec_unchecked(pred.as_bytes().to_vec()).into_raw() };
}
