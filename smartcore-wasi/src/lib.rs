use std::ffi::{CStr, CString};
use std::fs::File;
use std::io::{Read};
use std::mem;
use std::os::raw::{c_char, c_void};
// DenseMatrix wrapper around Vec
use smartcore::linalg::naive::dense_matrix::DenseMatrix;
// Linear Regression
use smartcore::linear::linear_regression::LinearRegression;


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
pub fn load_model(model_path: *mut c_char) -> *mut c_char {
    let path = unsafe { CStr::from_ptr(model_path).to_str().unwrap() };
    // let output_fname = CStr::from_ptr(output_ptr);
    let model: LinearRegression<f64, DenseMatrix<f64>> = {
        let mut buf: Vec<u8> = Vec::new();
        File::open(&path)
            .and_then(|mut f| f.read_to_end(&mut buf))
            .expect("Can not load model");
        bincode::deserialize(&buf).expect("Can not deserialize the model")
    };
    let data = DenseMatrix::from_array(1, 6, &[234.289, 235.6, 159.0, 107.608, 1947., 60.323]);

    let prediction = model.predict(&data).unwrap();
    let pred: String = prediction[0].to_string();
    return unsafe { CString::from_vec_unchecked(pred.as_bytes().to_vec()).into_raw() };
}
