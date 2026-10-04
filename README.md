# ReceiptSnap 🧾 - Receipt Analyzer & Bill Splitter

ReceiptSnap is an AI-powered Streamlit web application that allows users to upload receipt images or type out bill details, extract itemized breakdowns and totals using Gemini AI, calculate expense splits, and email the summary directly to their inbox.

---

## 📁 Project Structure

```text
receipt_splitter/
├── .streamlit/
│   └── secrets.toml.example   # Template for environment variables and secrets
├── .gitignore                  # Git ignore rules
├── app.py                     # Main Streamlit UI and application logic
├── prompts.py                 # System and user prompt templates
└── requirements.txt           # Python dependencies
```

---

## 🚀 Features

- **Receipt OCR & Analysis**: Upload JPEG/PNG images of receipts or paste bill text to get an instant breakdown of items, subtotal, tax, and final total.
- **Bill Splitting**: Specify names or number of people to calculate exact itemized or even splits.
- **Email Delivery**: Send structured expense summaries directly to your email using Gmail SMTP.
- **Session Chat Interface**: Continuous conversation UI to refine bill splits and ask follow-up questions.

---

## 🛠️ Prerequisites

- Python 3.9 or higher
- A Google Gemini API Key
- A Gmail account with an **App Password** enabled

---

## ⚙️ Installation & Setup

### 1. Clone or Extract Project
Extract `receipt_splitter_project.zip` or navigate into the root directory:
```bash
cd receipt_splitter
```

### 2. Set Up a Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration (`secrets.toml`)

Create a `secrets.toml` file inside the `.streamlit/` directory:

```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Open `.streamlit/secrets.toml` and fill in your details:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
GMAIL_ADDRESS = "your-sending-gmail@gmail.com"
GMAIL_APP_PASSWORD = "xxxx-xxxx-xxxx-xxxx"
```

> **Note on Gmail App Password**:
> 1. Go to your Google Account Settings (`myaccount.google.com`).
> 2. Enable **2-Step Verification**.
> 3. Search for **App Passwords** and generate a 16-character app password for "Mail". Use this password in `GMAIL_APP_PASSWORD`.

---

## 🏃 Running the Application

Launch the Streamlit app with:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📖 Usage Guide

1. **Onboarding**: Enter your name and email address when starting the app.
2. **Analyze Receipts**: Drag and drop a receipt photo into the chat input or type out bill items.
3. **Split Expenses**: Ask ReceiptSnap to split specific items or divide the total equally among friends.
4. **Email Summary**: Click the **📧 Send via Email** button at the top right to receive the full session report in your inbox.
