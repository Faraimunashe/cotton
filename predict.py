import pandas as pd
import joblib
import h5py
from sklearn.preprocessing import LabelEncoder, StandardScaler


h5_file = "best_svm_model.h5"
with h5py.File(h5_file, 'r') as f:
    joblib_file = f['model'][()]

model = joblib.load(joblib_file)


label_encoders = {}
categorical_columns = ['Gender', 'Married', 'Dependents', 'Self_Employed', 'Credit_History', 'Education', 'Property_Area']
for col in categorical_columns:
    le = LabelEncoder()
    label_encoders[col] = le

scaler = StandardScaler()

def preprocess_input(data, label_encoders, scaler):
    data = pd.DataFrame(data, index=[0])

    for col in categorical_columns:
        if data[col].isnull().any():
            data[col].fillna(data[col].mode()[0], inplace=True)

    numerical_columns = ['LoanAmount', 'Loan_Amount_Term']
    for col in numerical_columns:
        if data[col].isnull().any():
            data[col].fillna(data[col].mean(), inplace=True)

    for col in categorical_columns:
        le = label_encoders[col]
        data[col] = le.fit_transform(data[col])

    numerical_columns = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
    data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

    return data

def predict_loan_eligibility(input_data):
    processed_data = preprocess_input(input_data, label_encoders, scaler)
    prediction = model.predict(processed_data)
    return 'Approved' if prediction[0] == 1 else 'Rejected'


