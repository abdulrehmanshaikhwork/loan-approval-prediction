# ⚡ Quick Start Guide (30 Seconds)

Get the Loan Approval Prediction system running in just 30 seconds!

---

## 🪟 Windows

```bash
pip install -r requirements.txt
git clone https://github.com/abdulrehmanshaikhwork/loan-approval-prediction.git
cd loan-approval-prediction
python app.py
```

**Open**: http://localhost:5000

---

## 🍎 macOS

```bash
pip3 install -r requirements.txt
git clone https://github.com/abdulrehmanshaikhwork/loan-approval-prediction.git
cd loan-approval-prediction
python3 app.py
```

**Open**: http://localhost:5000

---

## 🐧 Linux (Ubuntu/Debian)

```bash
sudo apt-get install python3-pip
pip3 install -r requirements.txt
git clone https://github.com/abdulrehmanshaikhwork/loan-approval-prediction.git
cd loan-approval-prediction
python3 app.py
```

**Open**: http://localhost:5000

---

## ✅ Verify Installation

```bash
python main.py  # Train model if not already trained
python app.py   # Start web server
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

---

## 🎯 First Steps

1. **Enter Applicant Details** - Fill in age, income, credit score, etc.
2. **Click Predict** - Get instant default risk prediction
3. **Check Result** - See if applicant is eligible (Low/Medium/High risk)
4. **Download** - Save results to CSV (optional)

---

## 🚨 Troubleshooting

### Port Already in Use?
```bash
# Use a different port
python app.py --port 8080
```

### Model Not Found?
```bash
# Train the model first
python main.py
```

### Missing Dependencies?
```bash
# Reinstall all packages
pip install -r requirements.txt --force-reinstall
```

---

## 📊 Next Steps

- Read [FULL_GUIDE.md](FULL_GUIDE.md) for advanced features
- Check [API_GUIDE.md](API_GUIDE.md) for API integration
- See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for detailed setup

---

**That's it! You're ready to predict loan defaults! 🚀**
