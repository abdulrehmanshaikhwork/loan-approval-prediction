# 💻 Installation Guide for All Devices

Complete setup instructions for Windows, Mac, Linux, and cloud platforms.

---

## Table of Contents

1. [Windows Installation](#windows-installation)
2. [macOS Installation](#macos-installation)
3. [Linux Installation](#linux-installation)
4. [Network Setup](#-network-setup-guide)
5. [Mobile Support](#-mobile-support)
6. [Cloud Deployment](#-cloud-deployment)
7. [Common Issues](#-common-issues)

---

## Windows Installation

### Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/download/win))
- **Visual Studio Code** (Optional, [Download](https://code.visualstudio.com/))

### Step 1: Install Python

1. Download Python from https://www.python.org/downloads/
2. Run installer
3. ✅ **Check "Add Python to PATH"**
4. Click Install

### Step 2: Verify Python

Open **Command Prompt** and run:

```bash
python --version
pip --version
```

You should see version numbers printed.

### Step 3: Clone Repository

```bash
git clone https://github.com/abdulrehmanshaikhwork/loan-approval-prediction.git
cd loan-approval-prediction
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run Application

```bash
python main.py    # Train model (first time)
python app.py     # Start web server
```

### Step 6: Open in Browser

Visit: **http://localhost:5000**

---

## macOS Installation

### Prerequisites

- **Python 3.8+** (Usually pre-installed)
- **Git** ([Download](https://git-scm.com/download/mac))
- **Homebrew** (Optional, [Download](https://brew.sh/))

### Step 1: Verify Python

Open **Terminal** and run:

```bash
python3 --version
```

If not installed, install via Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

### Step 2: Verify Git

```bash
git --version
```

### Step 3: Clone Repository

```bash
git clone https://github.com/abdulrehmanshaikhwork/loan-approval-prediction.git
cd loan-approval-prediction
```

### Step 4: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 6: Run Application

```bash
python3 main.py    # Train model (first time)
python3 app.py     # Start web server
```

### Step 7: Open in Browser

Visit: **http://localhost:5000**

---

## Linux Installation

### Ubuntu/Debian

#### Prerequisites

```bash
sudo apt update
sudo apt install python3 python3-pip git
```

#### Installation Steps

```bash
# Clone repository
git clone https://github.com/abdulrehmanshaikhwork/loan-approval-prediction.git
cd loan-approval-prediction

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Run application
python3 main.py    # Train model
python3 app.py     # Start server
```

### RedHat/CentOS/Fedora

```bash
# Install Python
sudo dnf install python3 python3-pip git

# Follow Ubuntu steps above
```

### WSL (Windows Subsystem for Linux)

```bash
# Install WSL first from Windows Store
# Then follow Linux instructions above
```

---

## 🌐 Network Setup Guide

### Access From Different Devices

#### Find Your Computer's IP Address

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" (usually 192.168.x.x)

**Mac/Linux:**
```bash
ifconfig
```
Look for "inet" address under your active connection

#### Configure Flask to Accept Network Requests

Edit `app.py`:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

Then start the server:
```bash
python app.py
```

#### Access From Other Devices

Replace `192.168.1.100` with your actual computer IP:

- **Same Network**: `http://192.168.1.100:5000`
- **Android Phone**: Open Chrome → `http://192.168.1.100:5000`
- **iPhone**: Open Safari → `http://192.168.1.100:5000`
- **Another PC**: Open any browser → `http://192.168.1.100:5000`

#### Troubleshooting Network Access

```bash
# Check if port is open
netstat -an | findstr 5000  # Windows
lsof -i :5000               # Mac/Linux

# Disable firewall (temporary testing only)
# Windows: Settings → Firewall → Allow app through
```

---

## 📱 Mobile Support

### Android Phones

1. **Open Chrome** or Firefox
2. **Navigate to**: `http://192.168.1.100:5000`
3. **Add to Home Screen** (Optional):
   - Tap 3 dots → "Add to Home screen"
   - Now it works like an app!

### iPhone/iPad

1. **Open Safari**
2. **Navigate to**: `http://192.168.1.100:5000`
3. **Add to Home Screen** (Optional):
   - Tap share → "Add to Home Screen"
   - Now it works like an app!

### Progressive Web App (PWA)

The app can be installed as a PWA on supported browsers:

1. Open the app in Chrome/Edge
2. Address bar shows "Install" button
3. Click "Install"
4. App now has its own window

---

## ☁️ Cloud Deployment

### Heroku (Free Tier)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

heroku login
heroku create your-app-name
git push heroku main
heroku open
```

### AWS EC2

1. Create EC2 instance (Ubuntu 20.04)
2. SSH into instance:
```bash
ssh -i key.pem ec2-user@public-ip
```

3. Install Python & dependencies:
```bash
sudo yum update
sudo yum install python3 python3-pip git
git clone https://github.com/abdulrehmanshaikhwork/loan-approval-prediction.git
cd loan-approval-prediction
pip3 install -r requirements.txt
```

4. Run with Gunicorn:
```bash
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Google Cloud Run

```bash
# Create Dockerfile (already included)
gcloud run deploy loan-predictor \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### PythonAnywhere

1. Go to https://www.pythonanywhere.com/
2. Sign up (free account)
3. Upload files via Web tab
4. Configure Web app
5. Reload web app

### Replit

1. Go to https://replit.com/
2. Click "Create Repl"
3. Choose "Python"
4. Paste code
5. Click "Run"

---

## 🐛 Common Issues

### Issue: "Port 5000 already in use"

**Solution 1:** Use different port
```bash
python app.py --port 8080
```

**Solution 2:** Kill process using port
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

---

### Issue: "Module not found"

**Cause:** Missing dependencies

**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

---

### Issue: "Model not found"

**Cause:** Model file missing

**Solution:**
```bash
python main.py  # Train model first
```

---

### Issue: "Cannot connect to localhost:5000 from other device"

**Cause:** Firewall blocking port

**Solution:**
```bash
# Windows Firewall
Settings → Privacy & Security → Firewall → Allow app through

# macOS
System Preferences → Security & Privacy → Firewall Options

# Linux
sudo ufw allow 5000
```

---

### Issue: "Python command not found"

**Cause:** Python not in PATH

**Solution:**
```bash
# Windows: Reinstall Python with "Add to PATH" checked

# Mac: Use python3 instead of python
python3 --version

# Linux: Install Python
sudo apt install python3
```

---

### Issue: "Permission denied" on Linux/Mac

**Cause:** File permissions

**Solution:**
```bash
chmod +x *.py
chmod u+x app.py
```

---

### Issue: "Slow predictions"

**Cause:** Running in debug mode or slow CPU

**Solution:**
```python
# In app.py, change:
debug=False  # Not True

# Use production server:
pip install gunicorn
gunicorn -w 4 app:app
```

---

### Issue: "Port 5000 connection refused from network"

**Cause:** Flask only listening on localhost

**Solution:** Edit `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] Dependencies installed (`requirements.txt`)
- [ ] Model trained (`python main.py`)
- [ ] Server running (`python app.py`)
- [ ] Browser access working (http://localhost:5000)
- [ ] Form submission working
- [ ] Predictions loading correctly

---

## 📞 Still Having Issues?

1. **Check logs** in terminal for error messages
2. **Try reinstalling**: `pip install -r requirements.txt --force-reinstall`
3. **Check Python version**: Must be 3.8+
4. **Check internet connection**: For pip install
5. **Contact support**: GitHub Issues or Email

---

Next: [Full Guide](FULL_GUIDE.md) | [API Guide](API_GUIDE.md) | [Main README](README.md)
