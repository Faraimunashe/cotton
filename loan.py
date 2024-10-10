import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score

data = pd.read_csv('loan_dataset.csv')

data.fillna(method='ffill', inplace=True)

def prediction(applicant_data):
    label_encoder = LabelEncoder()
    data['employment_status'] = label_encoder.fit_transform(data['employment_status'])
    data['level_of_education'] = label_encoder.fit_transform(data['level_of_education'])

    numerical_features = ['income', 'debt_to_income_ratio', 'credit_score', 'loan_amount']
    X_numerical = data[numerical_features]

    scaler = StandardScaler()
    X_numerical_scaled = scaler.fit_transform(X_numerical)
    data[numerical_features] = X_numerical_scaled

    selected_features = ['income', 'credit_history', 'employment_status', 'debt_to_income_ratio', 'credit_score', 'loan_amount', 'level_of_education']

    X = data[selected_features]
    y = data['loan_status']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    example_data = applicant_data
    prediction = model.predict(example_data)
    print("Prediction:", prediction[0])
    return prediction[0]


prediction([[50000, 1, 1, 0.3, 700, 2000, 3]])