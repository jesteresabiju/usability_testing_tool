# 🧪 Usability Testing Tool

A Flask-based web app that automates usability testing for websites using Google Custom Search API and Selenium. Designed for speed, flexibility, and accuracy with dynamic test selection, live progress tracking, and PDF reporting.

---

## 🔍 Features

- ✅ **Test Features (per-site):**
  - Search Box
  - Navigation Bar
  - Contact Page / Link
  - Footer Presence
  - Login / Sign-in Option

- ⚡ **Performance:**
  - Parallel execution of tests using threads
  - Progress spinner with real-time completion updates

- 🧾 **Reporting:**
  - PDF report generation (per test run)
  - Optional email delivery via Gmail

- 🔄 **Fallback Logic:**
  - API-based detection first
  - Selenium fallback if API fails

- 🎛️ **User Control:**
  - Per-site test selection
  - Per-test configuration

---

## 🛠 Technologies Used

- **Python 3.x**
- **Flask** — Web framework
- **Selenium** — Browser automation
- **Google Custom Search API** — Primary content detection
- **FPDF** — PDF generation
- **Bootstrap 5** — UI styling (external HTML templates)

---

## 📁 Folder Structure

```none
usability_testing_tool/
├── app.py                   # Main Flask app
├── external_test_runner.py  # Background test logic
├── test_app.py              # Unit test module
├── utils/                   # Utility functions (e.g., API, Selenium)
├── templates/               # HTML templates (Jinja2)
├── static/                  # CSS, JS, spinner, report placeholder
├── pdf_reports/             # (Ignored) generated PDF reports
├── data/                    # Email + API config if needed
├── tests/                   # (Optional) for test scripts
├── requirements.txt
├── tasks.json
├── Procfile
├── .gitignore
└── README.md
`````
## 🚀 Getting Started

Follow these steps to set up and run the Usability Testing Tool locally.

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/jesteresabiju/usability_testing_tool.git
cd usability_testing_tool
```

---

### 2️⃣ Install Dependencies

Ensure you're using **Python 3.8+**, then install all required packages:

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configure API Keys and Email

Create a `config.py` file or set environment variables with the following:

```python
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'
GOOGLE_API_KEY = 'your_google_api_key'
SEARCH_ENGINE_ID = 'your_cse_id'
```

> 💡 If you're using Gmail with 2FA, make sure to [generate an App Password](https://support.google.com/accounts/answer/185833?hl=en).

---

### 4️⃣ Run the Flask App

```bash
python app.py
```

Now open your browser and visit:

```
http://localhost:5000
```

---

### 5️⃣ Start Testing

- Add website names and URLs
- Select the specific usability tests to run (e.g., Search, Navbar, Footer)
- Submit to view results and download the PDF report

---

✔️ You're all set! Let the testing begin.
