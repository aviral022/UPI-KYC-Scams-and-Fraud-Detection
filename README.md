<div align="center">

# 🛡️ FRAUD SHIELD

### Real-Time AI-Powered Scam & Fraud Intelligence System for India

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gemini AI](https://img.shields.io/badge/Google%20Gemini-AI%20Powered-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br>

**Report scams • Look up suspicious identifiers • Get AI-powered risk assessments**

*Built to combat the growing epidemic of digital fraud targeting Indian citizens*

---

</div>

## 🎯 The Problem

India faces an **unprecedented surge in digital fraud** — from UPI scams and fake KYC messages to sophisticated "digital arrest" schemes. Millions of citizens fall victim every year, losing crores to scammers who exploit trust, urgency, and technology gaps.

**Fraud Shield** is an intelligent, real-time fraud detection platform that empowers users to:

- 🚨 **Report** suspected scams with detailed context
- 🔎 **Look up** any phone number, UPI ID, email, or website to see if it's been flagged
- 🤖 **Get instant AI analysis** of suspicious messages and communications
- 📊 **Visualize trends** through a real-time analytics dashboard

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 📝 Smart Scam Reporting
Submit detailed fraud reports with identifier type, suspicious content, and personal notes. Each report is automatically analyzed and risk-scored.

</td>
<td width="50%">

### 🔍 Instant Identifier Lookup
Check if a phone number, UPI ID, website, or email has been previously reported. Get historical data and aggregated risk assessments.

</td>
</tr>
<tr>
<td width="50%">

### 🤖 Gemini AI Analysis
Leverages **Google Gemini 1.5 Flash** to deeply analyze suspicious content — identifying scam type, confidence level, and providing actionable advice.

</td>
<td width="50%">

### 📊 Live Analytics Dashboard
Real-time statistics covering total reports, risk distribution, top scam categories, identifier types, and recent flagged activity.

</td>
</tr>
<tr>
<td width="50%">

### 🧠 Multi-Factor Risk Engine
Proprietary scoring algorithm (0–100) combining keyword analysis, identifier pattern matching, report frequency, and AI confidence signals.

</td>
<td width="50%">

### 🇮🇳 India-Specific Intelligence
Purpose-built for Indian scam patterns: UPI fraud, KYC phishing, OTP theft, digital arrest, lottery scams, sextortion, fake job offers, and more.

</td>
</tr>
</table>

---

## �️ System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        FRAUD SHIELD                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐     ┌──────────────────────────────────┐     │
│   │   Frontend    │────▶│         FastAPI Backend           │     │
│   │  HTML/CSS/JS  │◀────│         (Uvicorn Server)          │     │
│   └──────────────┘     └───────┬──────────┬───────────────┘     │
│                                │          │                      │
│                    ┌───────────▼┐    ┌────▼──────────┐          │
│                    │  Risk       │    │  Gemini AI    │          │
│                    │  Engine     │    │  Service      │          │
│                    │  (0-100)    │    │  (Analysis)   │          │
│                    └──────┬─────┘    └───────┬───────┘          │
│                           │                  │                   │
│                    ┌──────▼──────────────────▼───────┐          │
│                    │        SQLite Database           │          │
│                    │   (Reports, Cache, Analytics)    │          │
│                    └─────────────────────────────────┘          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Fraud Detection/
│
├── 📂 backend/
│   ├── 🚀 main.py               # FastAPI app entry point & middleware
│   ├── 🗄️ database.py            # SQLite database layer (CRUD operations)
│   ├── 🤖 gemini_service.py      # Google Gemini AI integration & prompt engineering
│   ├── 🧠 risk_engine.py         # Multi-factor risk scoring algorithm
│   ├── 📋 schemas.py             # Pydantic models for request/response validation
│   ├── 📦 requirements.txt       # Python package dependencies
│   ├── 🔐 .env                   # Environment variables (API keys)
│   └── 📂 routes/
│       ├── 📝 reports.py         # POST/GET — Report submission & lookup
│       ├── 🔍 analysis.py        # POST — AI-powered scam analysis
│       └── 📊 dashboard.py       # GET — Aggregated statistics
│
├── 📂 frontend/
│   ├── 🌐 index.html             # Single-page application shell
│   ├── ⚡ app.js                  # Frontend logic, API calls, DOM rendering
│   └── 🎨 style.css              # Modern UI design with glassmorphism & animations
│
├── 🗃️ fraud_detection.db         # SQLite database (auto-created at runtime)
└── 📄 README.md                   # You are here!
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement       | Details                                                      |
|--------------------|--------------------------------------------------------------|
| **Python**         | Version 3.10 or higher                                       |
| **Gemini API Key** | Free from [Google AI Studio](https://aistudio.google.com/apikey) |

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/fraud-shield.git
cd fraud-shield
```

### 2️⃣ Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3️⃣ Configure Environment

Create or edit `backend/.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> 💡 **Tip:** The app works without an API key too — it falls back to pattern-based risk scoring only. AI analysis is a bonus!

### 4️⃣ Launch the Server

```bash
python main.py
```

### 5️⃣ Open in Browser

Navigate to **[http://localhost:8000](http://localhost:8000)** and start fighting fraud! 🎉

---

## 📡 REST API Reference

### Reports

| Method | Endpoint                | Description                                   |
|--------|-------------------------|-----------------------------------------------|
| `POST` | `/api/reports`          | Submit a new fraud report with full analysis   |
| `GET`  | `/api/reports`          | Retrieve all reports (paginated)               |
| `GET`  | `/api/lookup/{value}`   | Look up all reports matching an identifier     |

### Analysis

| Method | Endpoint                | Description                                   |
|--------|-------------------------|-----------------------------------------------|
| `POST` | `/api/analyze`          | Run AI-powered scam analysis on content        |

### Dashboard

| Method | Endpoint                | Description                                   |
|--------|-------------------------|-----------------------------------------------|
| `GET`  | `/api/dashboard`        | Aggregated stats, charts, and recent activity  |

<details>
<summary><b>📌 Example: Submit a Fraud Report</b></summary>

```bash
curl -X POST http://localhost:8000/api/reports \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_type": "phone",
    "identifier_value": "+91 9876543210",
    "description": "Received a call claiming to be from SBI asking for OTP to verify KYC. Threatened account freeze.",
    "reporter_name": "Anonymous"
  }'
```

**Response:**
```json
{
  "id": 1,
  "risk_score": 82,
  "risk_level": "CRITICAL",
  "risk_factors": ["OTP keyword detected", "KYC scam pattern", "Bank impersonation"],
  "ai_analysis": {
    "is_scam": true,
    "confidence": 0.95,
    "scam_type": "KYC / OTP Fraud",
    "explanation": "Classic KYC update scam targeting banking customers...",
    "advice": "Never share OTP with anyone. Banks never ask for OTP over call."
  }
}
```

</details>

---

## 🧠 Risk Scoring Engine — Deep Dive

The proprietary risk engine evaluates every report through **4 independent analysis layers** and produces a composite score from **0 to 100**:

```
┌─────────────────────────────────────────────────────────────┐
│                    RISK SCORE (0-100)                        │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  📝 Keyword  │  🔗 Pattern  │  📈 Frequency │  🤖 AI        │
│  Analysis    │  Matching    │  Analysis     │  Confidence   │
│  (30%)       │  (25%)       │  (20%)        │  (25%)        │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

| Layer | Weight | What It Does |
|-------|--------|-------------|
| **Keyword Analysis** | 30% | Scans for 30+ scam keywords — KYC, OTP, lottery, arrest, refund, Aadhaar, etc. |
| **Identifier Patterns** | 25% | Validates phone prefixes (TRAI 140-series), suspicious UPI handles, phishing URLs, disposable email domains |
| **Report Frequency** | 20% | Checks how many times the same identifier has been reported — repeat offenders score higher |
| **AI Confidence** | 25% | Google Gemini's scam classification confidence (0.0 – 1.0), when API key is available |

### Risk Levels

| Level | Score Range | Meaning |
|-------|:-----------:|---------|
| 🟢 **LOW** | 0 – 30 | Likely safe — no significant red flags |
| 🟡 **MEDIUM** | 31 – 60 | Suspicious — proceed with caution |
| 🟠 **HIGH** | 61 – 80 | Likely fraudulent — strong scam indicators |
| 🔴 **CRITICAL** | 81 – 100 | Confirmed scam pattern — do not engage |

---

## 🇮🇳 Scam Types Detected

Fraud Shield is trained to recognize the most prevalent scam categories targeting Indian citizens:

| Category | Description |
|----------|-------------|
| � **UPI Fraud** | Fake refund requests, malicious QR codes, unauthorized collect requests |
| 🏦 **KYC Scams** | Fake bank/Paytm/PhonePe KYC update messages with phishing links |
| 🔐 **OTP Theft** | Social engineering to steal one-time passwords for financial transactions |
| 💼 **Fake Jobs** | Work-from-home scams, fake placement agencies, task-based fraud |
| 🎰 **Lottery Scams** | Fake prize/lottery announcements demanding processing fees |
| 👮 **Digital Arrest** | Impersonating police/CBI/customs with video-call intimidation |
| 📈 **Investment Fraud** | Crypto/stock/trading scams with unrealistic return promises |
| 📱 **SIM Swap** | Fraudulent SIM replacement to take over banking accounts |
| 🆔 **ID Misuse** | Threats involving Aadhaar/PAN card data to create urgency |
| 📦 **Courier Scams** | Fake customs/delivery notifications demanding clearance fees |

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|:-----:|:----------:|:-------:|
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | High-performance async REST API |
| **AI Engine** | ![Gemini](https://img.shields.io/badge/Gemini%201.5%20Flash-4285F4?style=flat-square&logo=google&logoColor=white) | Scam classification & analysis |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) | Lightweight, zero-config storage |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) ![JS](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) | Modern responsive SPA |
| **Validation** | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white) | Schema validation & serialization |
| **Server** | ![Uvicorn](https://img.shields.io/badge/Uvicorn-2C2C2C?style=flat-square&logo=gunicorn&logoColor=white) | ASGI server with hot-reload |

</div>

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. 💻 **Commit** your changes: `git commit -m "Add amazing feature"`
4. 📤 **Push** to the branch: `git push origin feature/amazing-feature`
5. 🎉 **Open** a Pull Request

---

## � License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### Built with ❤️ by Aviral Dubey

*Empowering India's fight against digital fraud, one report at a time.*

⭐ **Star this repo** if you find it useful!

</div>
