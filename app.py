from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load the trained model bundle
MODEL_FILE = 'model.pkl'
model = None
threshold = 0.40  # Default threshold

if os.path.exists(MODEL_FILE):
    try:
        loaded = joblib.load(MODEL_FILE)
        # Handle both old format (Pipeline) and new format (dict/bundle)
        if isinstance(loaded, dict):
            # New bundle format
            model = loaded.get('model')
            threshold = loaded.get('threshold', 0.40)
            print(f"Model loaded from bundle. Threshold: {threshold}")
        else:
            # Old Pipeline format
            model = loaded
            threshold = 0.40
            print(f"Model loaded (legacy format). Using default threshold: {threshold}")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None
else:
    print("Model file not found. Please train the model first by running main.py")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({'status': 'error', 'message': 'Model not found. Please train the model first.'})
        
        # Get data from form
        form_data = request.form.to_dict()
        
        # Convert string inputs to appropriate types
        input_data = {
            'Age': int(form_data.get('age', 0)),
            'Income': float(form_data.get('income', 0)),
            'LoanAmount': float(form_data.get('loan_amount', 0)),
            'CreditScore': int(form_data.get('credit_score', 0)),
            'MonthsEmployed': int(form_data.get('employment_years', 0)) * 12,
            'NumCreditLines': int(form_data.get('credit_lines', 2)),
            'InterestRate': float(form_data.get('interest_rate', 5.0)),
            'LoanTerm': int(form_data.get('loan_term', 60)),
            'DTIRatio': float(form_data.get('debt_ratio', 0)) / 100,
            'EmploymentType': form_data.get('employment_type', 'Salaried'),
            'MaritalStatus': form_data.get('marital_status', 'Single'),
            'HasMortgage': form_data.get('has_mortgage', 'No'),
            'HasDependents': form_data.get('has_dependents', 'No'),
            'LoanPurpose': form_data.get('loan_purpose', 'Personal'),
            'HasCoSigner': form_data.get('has_cosigner', 'No'),
        }
        
        # Create DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Feature Engineering (same as in main.py)
        input_df["Loan_to_Income"] = input_df["LoanAmount"] / input_df["Income"]
        input_df["Estimated_EMI"] = (input_df["LoanAmount"] * input_df["InterestRate"]) / (12 * 100)
        input_df["EMI_to_Income"] = input_df["Estimated_EMI"] / input_df["Income"]
        input_df["High_DTI_Flag"] = (input_df["DTIRatio"] > 0.4).astype(int)
        input_df["Low_Credit_Flag"] = (input_df["CreditScore"] < 600).astype(int)
        input_df["Low_Employment_Stability"] = (input_df["MonthsEmployed"] < 12).astype(int)
        input_df["CreditLines_per_Age"] = input_df["NumCreditLines"] / input_df["Age"]
        input_df["Thin_Credit_File"] = (input_df["NumCreditLines"] <= 1).astype(int)
        input_df["Stable_Employment"] = input_df["EmploymentType"].isin(["Government", "Salaried"]).astype(int)
        input_df["Risk_Buffer"] = (
            (input_df["HasCoSigner"] == "Yes") |
            (input_df["MaritalStatus"] == "Married")
        ).astype(int)
        input_df["Education_Level"] = 1  # Default education level
        
        # Get probability predictions
        y_proba = model.predict_proba(input_df)[0]
        
        # Print probabilities for backend confirmation
        print(f"No Default Probability: {y_proba[0]:.4f}")
        print(f"Default Probability: {y_proba[1]:.4f}")
        
        default_prob = y_proba[1]  # Probability of default
        
        # Determine risk level and status based on threshold
        # Using threshold +/- 15% for boundaries
        low_risk_boundary = threshold - 0.15
        high_risk_boundary = threshold + 0.15
        
        if default_prob < low_risk_boundary:
            status = "✅ Low Default Risk – Eligible"
            risk_level = "Low"
            recommendation = "Eligible for loan approval"
        elif default_prob < high_risk_boundary:
            status = "⚠️ Medium Risk – Manual Review"
            risk_level = "Medium"
            recommendation = "Requires manual review by loan officer"
        else:
            status = "❌ High Risk – Not Eligible"
            risk_level = "High"
            recommendation = "Not eligible based on risk assessment"
        
        # Calculate risk percentage (invert to show non-default probability)
        risk_percentage = f"{default_prob * 100:.1f}%"
        approval_score = f"{(1 - default_prob) * 100:.1f}%"
        
        result = {
            'status': 'success',
            'prediction': status,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'default_probability': f"{default_prob:.4f}",
            'approval_score': approval_score,
            'risk_percentage': risk_percentage,
            'threshold_used': f"{threshold:.2f}"
        }
        
        return jsonify(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Prediction error: {str(e)}"})

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
