fn main() {
}

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
//     println!("MSE: {:#?}", mse);
// }