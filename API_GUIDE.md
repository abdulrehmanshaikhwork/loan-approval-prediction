# 🔌 API Guide

Complete API reference and integration guide for Loan Approval Prediction system.

---

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Request Format](#request-format)
5. [Response Format](#response-format)
6. [Error Handling](#error-handling)
7. [Integration Examples](#integration-examples)
8. [Rate Limiting](#rate-limiting)
9. [Webhooks](#webhooks)

---

## API Overview

### Base URL

```
http://localhost:5000
```

### API Features

- ✅ Real-time predictions
- ✅ RESTful architecture
- ✅ JSON request/response
- ✅ Error handling
- ✅ CORS support
- ✅ Batch processing
- ✅ File uploads

### Supported Methods

- `POST` - Create prediction
- `GET` - Retrieve data
- `PUT` - Update prediction (future)

---

## Authentication

### Current Version

No authentication required for local deployment.

### Production (Recommended)

Add API key authentication:

```python
# In app.py
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != 'your-secret-key':
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/predict', methods=['POST'])
@require_api_key
def predict():
    # ... prediction logic
```

### Usage with API Key

```bash
curl -X POST http://localhost:5000/predict \
  -H "X-API-Key: your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"age": 35, "income": 75000, ...}'
```

---

## Endpoints

### 1. Single Prediction

**Endpoint:** `POST /predict`

**Purpose:** Get default risk prediction for one applicant

**Request:**

```json
{
  "age": 35,
  "income": 75000,
  "loan_amount": 250000,
  "credit_score": 720,
  "employment_years": 5,
  "credit_lines": 4,
  "interest_rate": 6.5,
  "loan_term": 60,
  "debt_ratio": 35,
  "employment_type": "Salaried",
  "marital_status": "Married",
  "has_mortgage": "Yes",
  "has_dependents": "Yes",
  "loan_purpose": "Home",
  "has_cosigner": "No"
}
```

**Response (Success):**

```json
{
  "status": "success",
  "prediction": "✅ Low Default Risk – Eligible",
  "probability": 0.28,
  "risk_level": "Low",
  "recommendation": "ELIGIBLE",
  "confidence": 0.92,
  "processing_time_ms": 45
}
```

**Response (Error):**

```json
{
  "status": "error",
  "message": "Invalid input: age must be between 18 and 100",
  "error_code": "INVALID_INPUT"
}
```

---

### 2. Batch Prediction

**Endpoint:** `POST /batch-predict`

**Purpose:** Get predictions for multiple applicants

**Request:**

```json
{
  "applicants": [
    {
      "id": "APP001",
      "age": 35,
      "income": 75000,
      "loan_amount": 250000,
      "credit_score": 720,
      "employment_years": 5,
      "credit_lines": 4,
      "interest_rate": 6.5,
      "loan_term": 60,
      "debt_ratio": 35,
      "employment_type": "Salaried",
      "marital_status": "Married",
      "has_mortgage": "Yes",
      "has_dependents": "Yes",
      "loan_purpose": "Home",
      "has_cosigner": "No"
    },
    {
      "id": "APP002",
      "age": 28,
      "income": 55000,
      "loan_amount": 180000,
      "credit_score": 650,
      "employment_years": 2,
      "credit_lines": 2,
      "interest_rate": 8.5,
      "loan_term": 60,
      "debt_ratio": 42,
      "employment_type": "Salaried",
      "marital_status": "Single",
      "has_mortgage": "No",
      "has_dependents": "No",
      "loan_purpose": "Auto",
      "has_cosigner": "No"
    }
  ]
}
```

**Response:**

```json
{
  "status": "success",
  "total": 2,
  "predictions": [
    {
      "id": "APP001",
      "probability": 0.28,
      "risk_level": "Low",
      "recommendation": "ELIGIBLE"
    },
    {
      "id": "APP002",
      "probability": 0.58,
      "risk_level": "Medium",
      "recommendation": "REVIEW"
    }
  ],
  "summary": {
    "low_risk": 1,
    "medium_risk": 1,
    "high_risk": 0,
    "average_probability": 0.43
  }
}
```

---

### 3. File Upload & Predict

**Endpoint:** `POST /batch-upload`

**Purpose:** Upload CSV/Excel and get predictions for all

**Form Data:**

```
file: [CSV or Excel file]
```

**Example CSV File:**

```csv
age,income,loan_amount,credit_score,employment_years,credit_lines,interest_rate,loan_term,debt_ratio,employment_type,marital_status,has_mortgage,has_dependents,loan_purpose,has_cosigner
35,75000,250000,720,5,4,6.5,60,35,Salaried,Married,Yes,Yes,Home,No
28,55000,180000,650,2,2,8.5,60,42,Salaried,Single,No,No,Auto,No
45,95000,350000,780,15,6,5.5,84,28,Government,Married,Yes,Yes,Consolidation,No
```

**Response:**

```json
{
  "status": "success",
  "file_name": "applicants.csv",
  "total_records": 3,
  "processed": 3,
  "failed": 0,
  "predictions": [
    {
      "row": 0,
      "age": 35,
      "probability": 0.28,
      "risk_level": "Low"
    },
    {
      "row": 1,
      "age": 28,
      "probability": 0.58,
      "risk_level": "Medium"
    },
    {
      "row": 2,
      "age": 45,
      "probability": 0.21,
      "risk_level": "Low"
    }
  ],
  "summary": {
    "low_risk": 2,
    "medium_risk": 1,
    "high_risk": 0
  }
}
```

---

### 4. Health Check

**Endpoint:** `GET /health`

**Purpose:** Verify API is running

**Response:**

```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0",
  "timestamp": "2026-02-10T14:35:42"
}
```

---

### 5. Model Info

**Endpoint:** `GET /model-info`

**Purpose:** Get information about the model

**Response:**

```json
{
  "model_name": "Loan Default Predictor",
  "algorithm": "Logistic Regression",
  "version": "1.0",
  "training_data": "10000+ loan records",
  "accuracy": 0.85,
  "auc_roc": 0.88,
  "features": 15,
  "threshold": 0.40,
  "last_trained": "2026-02-10"
}
```

---

## Request Format

### Headers

```bash
Content-Type: application/json
X-API-Key: your-secret-key (optional)
```

### Content Types Supported

- `application/json` - JSON data
- `application/x-www-form-urlencoded` - Form data
- `multipart/form-data` - File upload

### Query Parameters

```bash
# Optional parameters
/predict?format=json&return_confidence=true
```

---

## Response Format

### Standard Response

```json
{
  "status": "success|error",
  "data": {},
  "message": "Description",
  "timestamp": "2026-02-10T14:35:42",
  "request_id": "req_abc123"
}
```

### Prediction Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "success" or "error" |
| `prediction` | string | Human-readable prediction |
| `probability` | float | 0-1 default probability |
| `risk_level` | string | Low/Medium/High |
| `recommendation` | string | ELIGIBLE/REVIEW/DECLINE |
| `confidence` | float | 0-1 confidence score |
| `processing_time_ms` | int | Response time |

### Error Response

```json
{
  "status": "error",
  "error_code": "INVALID_INPUT",
  "message": "Age must be between 18 and 100",
  "details": {
    "field": "age",
    "provided": -5,
    "expected": "18-100"
  }
}
```

---

## Error Handling

### Error Codes

| Code | HTTP | Description | Solution |
|------|------|-------------|----------|
| `INVALID_INPUT` | 400 | Bad request data | Check field values and types |
| `MODEL_ERROR` | 500 | Model not loaded | Ensure model.pkl exists |
| `FILE_ERROR` | 400 | Invalid file | Use CSV/Excel format |
| `SERVER_ERROR` | 500 | Unexpected error | Check server logs |
| `TIMEOUT` | 504 | Request too slow | Retry or use batch |

### Handling Errors in Code

```python
import requests

try:
    response = requests.post(
        'http://localhost:5000/predict',
        json=data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Risk: {result['risk_level']}")
    
    elif response.status_code == 400:
        error = response.json()
        print(f"Invalid input: {error['message']}")
    
    elif response.status_code == 500:
        print("Server error - try again later")

except requests.ConnectionError:
    print("Cannot connect to server")
except requests.Timeout:
    print("Request timed out")
```

---

## Integration Examples

### Python Integration

```python
import requests

class LoanPredictorClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
    
    def predict(self, **kwargs):
        """Single applicant prediction"""
        response = requests.post(
            f'{self.base_url}/predict',
            json=kwargs
        )
        return response.json()
    
    def batch_predict(self, applicants):
        """Multiple applicants prediction"""
        response = requests.post(
            f'{self.base_url}/batch-predict',
            json={'applicants': applicants}
        )
        return response.json()

# Usage
client = LoanPredictorClient()
result = client.predict(
    age=35,
    income=75000,
    loan_amount=250000,
    credit_score=720,
    employment_years=5,
    credit_lines=4,
    interest_rate=6.5,
    loan_term=60,
    debt_ratio=35,
    employment_type='Salaried',
    marital_status='Married',
    has_mortgage='Yes',
    has_dependents='Yes',
    loan_purpose='Home',
    has_cosigner='No'
)
print(result['risk_level'])
```

### JavaScript Integration

```javascript
async function predictLoan(applicantData) {
  const response = await fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(applicantData)
  });
  
  const result = await response.json();
  
  if (result.status === 'success') {
    console.log(`Risk Level: ${result.risk_level}`);
    console.log(`Probability: ${result.probability}`);
    console.log(`Recommendation: ${result.recommendation}`);
  } else {
    console.error(`Error: ${result.message}`);
  }
}

// Usage
const applicant = {
  age: 35,
  income: 75000,
  loan_amount: 250000,
  credit_score: 720,
  employment_years: 5,
  credit_lines: 4,
  interest_rate: 6.5,
  loan_term: 60,
  debt_ratio: 35,
  employment_type: 'Salaried',
  marital_status: 'Married',
  has_mortgage: 'Yes',
  has_dependents: 'Yes',
  loan_purpose: 'Home',
  has_cosigner: 'No'
};

predictLoan(applicant);
```

### cURL Examples

```bash
# Single prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "income": 75000,
    "loan_amount": 250000,
    "credit_score": 720,
    "employment_years": 5,
    "credit_lines": 4,
    "interest_rate": 6.5,
    "loan_term": 60,
    "debt_ratio": 35,
    "employment_type": "Salaried",
    "marital_status": "Married",
    "has_mortgage": "Yes",
    "has_dependents": "Yes",
    "loan_purpose": "Home",
    "has_cosigner": "No"
  }'

# File upload
curl -X POST http://localhost:5000/batch-upload \
  -F "file=@applicants.csv"

# Health check
curl http://localhost:5000/health
```

### Excel VBA Integration

```vba
Function PredictLoan(age, income, loanAmount, creditScore) As String
    Dim xmlHttp As Object
    Dim url As String
    Dim jsonData As String
    
    Set xmlHttp = CreateObject("MSXML2.XMLHTTP")
    
    url = "http://localhost:5000/predict"
    
    jsonData = "{" & _
        """age"": " & age & "," & _
        """income"": " & income & "," & _
        """loan_amount"": " & loanAmount & "," & _
        """credit_score"": " & creditScore & _
    "}"
    
    With xmlHttp
        .Open "POST", url, False
        .setRequestHeader "Content-Type", "application/json"
        .send jsonData
        PredictLoan = .responseText
    End With
End Function

' Usage in Excel:
' =PredictLoan(35, 75000, 250000, 720)
```

### Power BI Integration

```powerquery
let
  Source = Json.Document(
    Web.Contents(
      "http://localhost:5000/batch-predict",
      [Content = Text.ToBinary(
        Json.FromValue([applicants = applicantData])
      )]
    )
  )
in
  Source[predictions]
```

### Salesforce Integration

```apex
public class LoanPredictorService {
    public static LoanPrediction predictDefault(String applicantJson) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('http://localhost:5000/predict');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setBody(applicantJson);
        
        Http http = new Http();
        HttpResponse response = http.send(req);
        
        return (LoanPrediction) JSON.deserialize(
            response.getBody(),
            LoanPrediction.class
        );
    }
}

public class LoanPrediction {
    public String status;
    public String risk_level;
    public Double probability;
    public String recommendation;
}
```

---

## Rate Limiting

### Current Implementation

No rate limiting in local version.

### Production Recommended Limits

```python
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["200/day", "50/hour"]
)

@app.route('/predict', methods=['POST'])
@limiter.limit("10/minute")
def predict():
    # ... prediction logic
```

---

## Webhooks

### Setup (Future Feature)

Send predictions to external service:

```python
@app.route('/predict', methods=['POST'])
def predict():
    # ... prediction logic
    
    # Send webhook notification
    if result['probability'] > 0.65:
        notify_webhook({
            'event': 'HIGH_RISK_DETECTED',
            'applicant_id': applicant_id,
            'probability': result['probability']
        })
```

---

## Monitoring & Logging

### View API Logs

Logs are printed to console:

```
[2026-02-10 14:35:42] POST /predict - 200 OK
[2026-02-10 14:35:42] Input validated
[2026-02-10 14:35:42] Features engineered
[2026-02-10 14:35:42] Prediction: 0.28 (Low Risk)
[2026-02-10 14:35:42] Response sent in 45ms
```

### API Metrics

Track calls per day:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    logger.info(f"Prediction request from {request.remote_addr}")
    # ... rest of code
    logger.info(f"Prediction completed in {time}ms")
```

---

## API Versioning

Current version: **v1.0**

Future versions will support:
- `/api/v1/predict`
- `/api/v2/predict` (new features)
- Backward compatibility maintained

---

**Next:** [Full Guide](FULL_GUIDE.md) | [Installation](INSTALLATION_GUIDE.md) | [README](README.md)
