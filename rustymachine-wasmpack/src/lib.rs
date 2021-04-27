mod utils;

use wasm_bindgen::prelude::*;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

#[wasm_bindgen]
pub fn greet() {
    log("Hello, nodejs-rust!");
}

// use rustlearn::cross_validation::CrossValidation;
// use rustlearn::datasets::iris;
// use rustlearn::linear_models::sgdclassifier::Hyperparameters;
// use rustlearn::metrics::accuracy_score;
// use rustlearn::prelude::*;

// #[wasm_bindgen]
// pub fn fit_accuracy() -> f32 {
//     let (x, y) = iris::load_data();

//     let num_splits = 10;
//     let num_epochs = 5;
//     let mut accuracy = 0.0;
//     for (train_idx, test_idx) in CrossValidation::new(x.rows(), num_splits) {
//         let x_train = x.get_rows(&train_idx);
//         let y_train = y.get_rows(&train_idx);
//         let x_test = x.get_rows(&test_idx);
//         let y_test = y.get_rows(&test_idx);
//         let mut model = Hyperparameters::new(x.cols())
//             .learning_rate(0.5)
//             .l2_penalty(0.0)
//             .l1_penalty(0.0)
//             .one_vs_rest();
//         for _ in 0..num_epochs {
//             model.fit(&x_train, &y_train).unwrap();
//         }
//         let prediction = model.predict(&x_test).unwrap();
//         accuracy += accuracy_score(&y_test, &prediction);
//     }
//     accuracy /= num_splits as f32;
//     return accuracy;
// }

// use smartcore::dataset::*;
// // DenseMatrix wrapper around Vec
// use smartcore::linalg::naive::dense_matrix::DenseMatrix;
// // Linear Regression
// use smartcore::linear::linear_regression::LinearRegression;
// // Model performance
// use smartcore::metrics::accuracy::Accuracy;
// use smartcore::metrics::mean_squared_error;
// use smartcore::model_selection::train_test_split;

// // Load dataset
// #[wasm_bindgen]
// pub fn model() {
//     let cancer_data = boston::load_dataset();
//     // Transform dataset into a NxM matrix
//     let x = DenseMatrix::from_array(
//         cancer_data.num_samples,
//         cancer_data.num_features,
//         &cancer_data.data,
//     );
//     // These are our target class labels
//     let y = cancer_data.target;
//     // Split dataset into training/test (80%/20%)
//     let (x_train, x_test, y_train, y_test) = train_test_split(&x, &y, 0.2, true);
//     // Linear Regression
//     let model = LinearRegression::fit(&x_train, &y_train, Default::default()).unwrap();
//     let pred = model.predict(&x_test).unwrap();
    
//     let mse = mean_squared_error(&pred, &y_test);
//     return
// }

use rusty_machine::learning::logistic_reg::LogisticRegressor;
use rusty_machine::learning::SupModel;
use rusty_machine::linalg::Matrix;
use rusty_machine::linalg::Vector;

#[wasm_bindgen]
pub fn basic_prediction(data: Vec<f64>) -> Vec<f64>{
    let inputs = Matrix::new(4, 1, vec![1.0, 3.0, 5.0, 7.0]);
    let targets = Vector::new(vec![0., 0., 1., 1.]);
    let mut log_mod = LogisticRegressor::default();
    log_mod.train(&inputs, &targets).unwrap();
    let new_point = Matrix::new(data.len(), 1, data);
    let output = log_mod.predict(&new_point).unwrap();
    return output.into_vec();
}
