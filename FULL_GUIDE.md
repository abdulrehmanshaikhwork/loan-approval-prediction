# 📖 Full Documentation Guide

Complete feature documentation and usage guide for Loan Approval Prediction system.

---

## Table of Contents

1. [Application Overview](#application-overview)
2. [Features Explained](#features-explained)
3. [How the Model Works](#how-the-model-works)
4. [Input Features](#input-features)
5. [Output Predictions](#output-predictions)
6. [Using the Web Interface](#using-the-web-interface)
7. [Data Processing](#data-processing)
8. [Model Training](#model-training)
9. [Advanced Usage](#advanced-usage)

---

## Application Overview

### What It Does

The Loan Approval Prediction system uses machine learning to analyze loan applicant data and predict the probability of loan default. It provides:

- **Real-time predictions** on whether an applicant will default
- **Risk categorization** (Low/Medium/High risk)
- **Confidence scores** showing prediction certainty
- **Actionable insights** for loan officers

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.8+ Flask 2.3.3 |
| ML Model | Scikit-learn Logistic Regression |
| Data Processing | Pandas, NumPy |
| Frontend | HTML5, CSS3, Bootstrap |
| Database | CSV files (no database required) |
| Deployment | Docker, Cloud platforms |

---

## Features Explained

### Feature 1: Single Applicant Prediction

**How to use:**

1. Click "Single Prediction" tab
2. Fill in all applicant details:
   - **Demographics**: Age, Marital Status
   - **Financial**: Income, Loan Amount, Debt Ratio
   - **Credit**: Credit Score, Number of Credit Lines
   - **Employment**: Employment Type, Years Employed
   - **Loan Details**: Loan Term, Interest Rate, Loan Purpose
   - **Assets**: Mortgage, Co-signer, Dependents

3. Click "Predict" button
4. Results show instantly with:
   - Default probability (0-100%)
   - Risk level indicator
   - Recommendation (Eligible/Review/Decline)

**Example:**
```
Age: 35
Income: $75,000
Credit Score: 720
Loan Amount: $250,000

Result: ✅ LOW RISK - Eligible
Probability: 28% default risk
```

---

### Feature 2: Batch Predictions

**How to use:**

1. Click "Batch Prediction" tab
2. Add multiple applicants manually:
   - Click "Add Applicant"
   - Fill in details
   - Click "Save"
   - Repeat for more applicants

3. Click "Predict All"
4. See results in table format with:
   - Each applicant's details
   - Their risk level
   - Default probability
   - Overall statistics

**Features:**
- Sort by any column
- Filter by risk level
- Download as CSV
- Visual risk distribution

---

### Feature 3: File Upload

**How to use:**

1. Click "File Upload" tab
2. Prepare CSV/Excel file with columns:
   - Age, Income, LoanAmount, CreditScore
   - MonthsEmployed, NumCreditLines, InterestRate
   - LoanTerm, DTIRatio, EmploymentType
   - MaritalStatus, HasMortgage, HasDependents
   - LoanPurpose, HasCoSigner

3. Click "Browse" and select file
4. Click "Upload & Predict"
5. System processes all rows and shows:
   - Total applicants processed
   - Risk distribution (Low/Medium/High)
   - Predictions table
   - Download results

**Example File Format:**
```csv
Age,Income,LoanAmount,CreditScore,MonthsEmployed,NumCreditLines
35,75000,250000,720,60,4
28,55000,180000,650,24,2
45,95000,350000,780,180,5
```

---

## How the Model Works

### Model Architecture

```
Input Data (15 Features)
        ↓
Data Validation
        ↓
Feature Engineering (13+ computed features)
        ↓
Feature Scaling (StandardScaler)
        ↓
Logistic Regression Model
        ↓
Probability Output (0-1)
        ↓
Risk Classification
        ↓
Recommendation
```

### Feature Engineering

The model creates advanced features from raw input:

| Feature | Calculation | Purpose |
|---------|-----------|---------|
| **Loan_to_Income** | LoanAmount / Income | Affordability |
| **Estimated_EMI** | (LoanAmount × InterestRate) / (12 × 100) | Monthly payment |
| **EMI_to_Income** | Estimated_EMI / Income | Payment burden |
| **High_DTI_Flag** | 1 if DTI > 40%, else 0 | Risk indicator |
| **Low_Credit_Flag** | 1 if Score < 600, else 0 | Credit risk |
| **Low_Employment_Stability** | 1 if Months < 12, else 0 | Job stability |
| **CreditLines_per_Age** | NumCreditLines / Age | Credit history |
| **Thin_Credit_File** | 1 if Lines ≤ 1, else 0 | Limited history |
| **Stable_Employment** | 1 if Gov/Salaried, else 0 | Income stability |
| **Risk_Buffer** | 1 if CoSigner/Married, else 0 | Safety net |

### Prediction Process

1. **Input Validation**: Check all fields are valid
2. **Preprocessing**: Convert strings to numbers
3. **Feature Engineering**: Create derived features
4. **Scaling**: Normalize numerical features
5. **Model Prediction**: Get probability (0-1)
6. **Classification**: Map probability to risk level

### Risk Levels

| Probability | Risk Level | Recommendation |
|------------|-----------|----------------|
| < 25% | 🟢 **Low** | ✅ **Approve** |
| 25-40% | 🟡 **Low-Medium** | ✅ **Approve** |
| 40-55% | 🟠 **Medium** | ⚠️ **Review** |
| 55-65% | 🔴 **Medium-High** | ⚠️ **Review** |
| > 65% | 🔴 **High** | ❌ **Decline** |

---

## Input Features

### Demographics

**Age**
- Range: 18-80 years
- Impact: Younger applicants have higher risk
- Format: Integer

**Marital Status**
- Options: Single, Married, Divorced, Widowed
- Impact: Married status reduces risk
- Format: Dropdown

### Financial Information

**Annual Income**
- Range: $0-$999,999
- Impact: Higher income reduces risk
- Format: Currency (no $ symbol needed)

**Loan Amount**
- Range: $1,000-$999,999
- Impact: Higher loan increases risk
- Format: Currency

**Debt-to-Income (DTI) Ratio**
- Range: 0-100%
- Impact: Higher ratio increases risk
- Format: Percentage
- Calculation: Total debt payments / Monthly income

### Credit Information

**Credit Score**
- Range: 300-850 (FICO scale)
- Impact: Higher score reduces risk significantly
- Format: Integer
- Thresholds:
  - Below 600: Poor credit
  - 600-700: Fair credit
  - 700+: Good credit

**Number of Credit Lines**
- Range: 1-10
- Impact: More lines = established credit
- Format: Integer

### Employment Information

**Employment Type**
- Options: Salaried, Government, Self-Employed, Freelance, Retired
- Impact: Government/Salaried = most stable
- Format: Dropdown

**Months Employed**
- Range: 0-600 months (50 years)
- Impact: Longer employment reduces risk
- Format: Integer (calculated from years)
- Conversion: Years × 12 = Months

### Loan Details

**Interest Rate**
- Range: 2-25% p.a.
- Impact: Higher rate = Riskier applicant
- Format: Percentage

**Loan Term**
- Range: 12-360 months (1-30 years)
- Impact: Longer terms increase risk
- Format: Integer

**Loan Purpose**
- Options: Home, Auto, Education, Business, Personal, Consolidation
- Impact: Home loans = lower risk
- Format: Dropdown

### Asset/Guarantee Information

**Has Mortgage**
- Options: Yes, No
- Impact: Asset backing reduces risk
- Format: Dropdown

**Has Dependents**
- Options: Yes, No
- Impact: Dependents may increase risk
- Format: Dropdown

**Has Co-Signer**
- Options: Yes, No
- Impact: Co-signer reduces risk
- Format: Dropdown

---

## Output Predictions

### Prediction Output

For each applicant, you get:

**1. Risk Level**
```
✅ Low Default Risk – Eligible
🟠 Medium Default Risk – Review Required
❌ High Default Risk – Likely to Default
```

**2. Default Probability**
```
Example: 28% probability of default
0% = Very safe
100% = Very risky
```

**3. Confidence Score**
Shows how confident the model is in its prediction.

**4. Recommendation**
- **ELIGIBLE**: Can approve immediately
- **REVIEW**: Manual underwriting needed
- **DECLINE**: High risk, recommend decline

### Result Example

```
APPLICANT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name: John Doe
Age: 35
Income: $75,000
Credit Score: 720
Loan Amount: $250,000

RESULT: ✅ LOW DEFAULT RISK – ELIGIBLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Default Probability: 28% ▮▮▮▮▮░░░░░
Risk Level: LOW
Status: ELIGIBLE FOR APPROVAL

KEY FACTORS:
✅ Good credit score (720)
✅ Stable employment (Salaried, 5 years)
✅ Reasonable debt ratio (35%)
⚠️ Slight concern: Loan amount is 3.3x annual income
```

---

## Using the Web Interface

### Step-by-Step Tutorial

#### Step 1: Access the Application

1. Start the server:
```bash
python app.py
```

2. Open web browser
3. Navigate to: **http://localhost:5000**

#### Step 2: Navigate Tabs

Three main tabs available:
- **Single Prediction** - Predict one applicant
- **Batch Prediction** - Predict multiple at once
- **File Upload** - Upload CSV/Excel

#### Step 3: Fill Form

For single prediction:

1. **Personal Details**
   - Age: 35
   - Marital Status: Married

2. **Income Details**
   - Income: 75000
   - Debt Ratio: 35

3. **Credit Details**
   - Credit Score: 720
   - Credit Lines: 4

4. **Employment Details**
   - Type: Salaried
   - Years Employed: 5

5. **Loan Details**
   - Amount: 250000
   - Term: 60 months
   - Interest Rate: 6.5
   - Purpose: Home

6. **Additional Info**
   - Has Mortgage: Yes
   - Has Dependents: Yes
   - Has Co-Signer: No

#### Step 4: Submit

Click **"PREDICT"** button

#### Step 5: View Results

See:
- Risk level with emoji indicator
- Default probability percentage
- Status recommendation
- Advice for next steps

#### Step 6: Download (Optional)

Click **"Download as CSV"** to save results

---

## Data Processing

### Data Validation

Before prediction, system validates:

✓ All fields are filled  
✓ Numbers are in valid ranges  
✓ Age: 18-100  
✓ Income: > 0  
✓ Credit Score: 300-850  
✓ Percentages: 0-100  

### Data Transformation

```python
# Example transformation for batch
input_values = {
    'Age': 35,
    'Income': 75000,
    'LoanAmount': 250000,
    # ... other fields
}

# Convert to DataFrame
df = pd.DataFrame([input_values])

# Feature engineering
df['Loan_to_Income'] = df['LoanAmount'] / df['Income']
df['Estimated_EMI'] = (df['LoanAmount'] * df['InterestRate']) / (12 * 100)
# ... more features

# Scale numerical features
df_scaled = scaler.transform(df[numerical_features])

# Predict
probability = model.predict_proba(df_scaled)
```

### Output Format

Results are provided in multiple formats:

**Web Display:**
```
✅ LOW RISK: 28% default probability
```

**CSV Export:**
```csv
Name,Age,Income,CreditScore,RiskLevel,Probability
John Doe,35,75000,720,Low,0.28
```

**JSON API:**
```json
{
  "status": "success",
  "risk_level": "Low",
  "probability": 0.28,
  "recommendation": "ELIGIBLE"
}
```

---

## Model Training

### Training Process

Use `main.py` to train the model:

```bash
python main.py
```

Training steps:

1. **Load Data** (Loan_default.csv)
   - 10,000+ loan records
   - 15 features
   - Default/No-default labels

2. **Exploration** (01-05 notebooks)
   - Analyze data patterns
   - Check for missing values
   - Understand feature distributions

3. **Feature Engineering** (02 notebook)
   - Create derived features
   - Handle categorical variables
   - Scale numerical values

4. **Build Pipeline** (06 notebook)
   - Preprocessing steps
   - Model selection
   - Cross-validation

5. **Train Model** (07 notebook)
   - Logistic Regression
   - Hyperparameter tuning
   - Model evaluation

6. **Save Model** (main.py)
   - Save as `model.pkl`
   - Used by `app.py`

### Training Data

**Dataset:** Loan_default.csv

| Metric | Value |
|--------|-------|
| Total Records | 10,000+ |
| Features | 15 |
| Target Variable | Default (0/1) |
| Default Rate | ~30% |

**Train-Test Split:** 80-20  
**Scaling:** StandardScaler  
**Encoding:** OneHotEncoder  

### Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 85%+ |
| Precision | 0.82 |
| Recall | 0.88 |
| F1-Score | 0.85 |
| AUC-ROC | 0.88 |

---

## Advanced Usage

### Using the API Programmatically

```python
import requests
import json

# Single prediction
url = "http://localhost:5000/predict"
data = {
    'age': 35,
    'income': 75000,
    'loan_amount': 250000,
    'credit_score': 720,
    'employment_years': 5,
    'credit_lines': 4,
    'interest_rate': 6.5,
    'loan_term': 60,
    'debt_ratio': 35,
    'employment_type': 'Salaried',
    'marital_status': 'Married',
    'has_mortgage': 'Yes',
    'has_dependents': 'Yes',
    'loan_purpose': 'Home',
    'has_cosigner': 'No'
}

response = requests.post(url, data=data)
result = response.json()
print(f"Risk Level: {result['risk_level']}")
print(f"Probability: {result['probability']}")
```

### Batch Processing Script

```python
import pandas as pd
from flask import Flask
import joblib

# Load model
model = joblib.load('model.pkl')

# Load data
df = pd.read_csv('applicants.csv')

# Process each applicant
predictions = []
for idx, row in df.iterrows():
    # Feature engineering
    features = engineer_features(row)
    
    # Predict
    prob = model.predict_proba([features])[0][1]
    risk_level = categorize_risk(prob)
    
    predictions.append({
        'applicant_id': row['id'],
        'probability': prob,
        'risk_level': risk_level
    })

# Save results
results_df = pd.DataFrame(predictions)
results_df.to_csv('predictions.csv', index=False)
```

### Custom Threshold

Adjust risk threshold in `app.py`:

```python
# Change threshold from 0.40 to 0.35
threshold = 0.35

if default_prob < threshold - 0.15:
    status = "Low Risk"
elif default_prob < threshold + 0.15:
    status = "Medium Risk"
else:
    status = "High Risk"
```

### Integration with CRM

```python
# Example: Salesforce integration
import requests

# Get loan predictions
prediction = get_prediction(applicant_data)

# Update Salesforce
sf_api = "https://your-instance.salesforce.com/services/data/v57.0"
requests.patch(
    f"{sf_api}/sobjects/Opportunity/{opportunity_id}",
    json={
        'LoanDefaultRisk__c': prediction['probability'],
        'RiskLevel__c': prediction['risk_level']
    }
)
```

---

### Monitoring & Logging

The app logs predictions:

```
[2026-02-10 14:35:42] Prediction requested
[2026-02-10 14:35:42] Input: Age=35, Income=75000, CreditScore=720
[2026-02-10 14:35:42] Default Probability: 0.28
[2026-02-10 14:35:42] Risk Level: Low
[2026-02-10 14:35:42] Status: Eligible
[2026-02-10 14:35:43] Response sent
```

View logs in terminal where Flask is running.

---

## Configuration Options

### Flask Configuration

Edit `app.py`:

```python
app.config['DEBUG'] = False              # Disable debug
app.config['JSON_SORT_KEYS'] = False     # Don't sort JSON
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Pretty JSON
```

### Model Configuration

Edit `main.py`:

```python
# Change model threshold
FINAL_THRESHOLD = 0.40

# Change random seed
random_seed = 42

# Adjust test split
test_size = 0.20
```

---

## Performance Optimization

### For Better Accuracy

1. Collect more training data
2. Add more features (debt history, payment history)
3. Try other algorithms (XGBoost, Random Forest)
4. Hyperparameter tuning
5. Class balancing techniques

### For Faster Predictions

1. Use Gunicorn server:
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

2. Enable caching:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

3. Use model quantization:
```python
# Reduce model size
import joblib
compressed = joblib.dump(model, 'model.pkl', compress=3)
```

---

**Next Steps:** [Quick Start](QUICK_START.md) | [Installation Guide](INSTALLATION_GUIDE.md) | [API Guide](API_GUIDE.md)
