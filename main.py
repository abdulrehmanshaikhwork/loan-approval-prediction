import pandas as pd
import os
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    roc_auc_score,
    classification_report,
    confusion_matrix
)
from torch import threshold

MODEL_FILE = 'model.pkl'
FINAL_THRESHOLD = 0.40

def build_pipeline(num_attribs, cat_attribs):
    num_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", drop="first"))
    
    ])
    
    preprocessor = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", cat_pipeline, cat_attribs)
])
    
    return preprocessor

if not os.path.exists(MODEL_FILE):
    print("Model not found. Running the training phase first.")

    # Load the data
    df = pd.read_csv("Loan_default.csv")

    # Drop the LoanID column as it is not useful for prediction
    df = df.drop(columns=["LoanID"])

    # Creating Useful Columns
    df["Loan_to_Income"] = df["LoanAmount"] / df["Income"]
    df["Estimated_EMI"] = (df["LoanAmount"] * df["InterestRate"]) / (12 * 100)
    df["EMI_to_Income"] = df["Estimated_EMI"] / df["Income"]
    df["High_DTI_Flag"] = (df["DTIRatio"] > 0.4).astype(int)
    df["Low_Credit_Flag"] = (df["CreditScore"] < 600).astype(int)
    df["Low_Employment_Stability"] = (df["MonthsEmployed"] < 12).astype(int)
    df["CreditLines_per_Age"] = df["NumCreditLines"] / df["Age"]
    df["Thin_Credit_File"] = (df["NumCreditLines"] <= 1).astype(int)
    df["Stable_Employment"] = df["EmploymentType"].isin(
    ["Government", "Salaried"]
    ).astype(int)
    df["Risk_Buffer"] = (
    (df["HasCoSigner"] == "Yes") |
    (df["MaritalStatus"] == "Married")
    ).astype(int)
    education_map = {
    "High School": 0,
    "Bachelor's": 1,
    "Master's": 2,
        "PhD": 3
    }

    df["Education_Level"] = df["Education"].map(education_map)
    df.drop(columns=["Education"], inplace=True)

    # Define features and target
    x = df.drop(columns=["Default"])
    y = df["Default"]

    # identify numeric and categorical columns
    num_attribs = [
    "Age",
    "Income",
    "LoanAmount",
    "CreditScore",
    "MonthsEmployed",
    "NumCreditLines",
    "InterestRate",
    "LoanTerm",
    "DTIRatio",

    # Engineered features
    "Loan_to_Income",
    "Estimated_EMI",
    "EMI_to_Income",
    "High_DTI_Flag",
    "Low_Credit_Flag",
    "Low_Employment_Stability",
    "CreditLines_per_Age",
    "Thin_Credit_File",
    "Stable_Employment",
    "Risk_Buffer",
    "Education_Level"
    ]


    cat_attribs = [
        "EmploymentType",
        "MaritalStatus",
        "HasMortgage",
        "HasDependents",
        "LoanPurpose",
        "HasCoSigner"
    ]


    # Split the data into training and testing sets
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_idx, test_idx in split.split(x,y):
        x_train = x.iloc[train_idx]
        x_test = x.iloc[test_idx]

        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        x_test.to_csv("input.csv", index=False)

    preprocessor = build_pipeline(num_attribs, cat_attribs)

    
    model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(
        class_weight='balanced',
        max_iter=1000,
        random_state=42
    ))
    ])

    # Train
    model.fit(x_train, y_train)

    y_proba = model.predict_proba(x_test)[:, 1]
    print("ROC-AUC:", roc_auc_score(y_test, y_proba))

    # Save the model
    model_bundle ={
        'model': model,
        'threshold': FINAL_THRESHOLD
    }
    joblib.dump(model_bundle, MODEL_FILE) 

    print("Model trained and saved.")

# Inference phase
else:
    print("Model found. Running the inference phase.")

    # Load the model
    bundle = joblib.load(MODEL_FILE)

    model = bundle["model"]
    threshold = bundle["threshold"]

    # Load new input data for inference
    input_data = pd.read_csv("input.csv")

    # Predict probabilities
    y_proba = model.predict_proba(input_data)[:, 1]

    y_pred = (y_proba >= threshold).astype(int)

    # Save predictions to output.csv
    input_data["Default_Probability"] = y_proba
    input_data["Default_Prediction"] = y_pred
    input_data.to_csv("output.csv", index=False)
    print("Inference complete. Results saved to output.csv")

    


