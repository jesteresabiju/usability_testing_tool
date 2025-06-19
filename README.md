# Usability Testing Tool

A Flask-based web app to run automated usability tests on websites using Google API and Selenium.

## 🔍 Features

- Detects presence of:
  - Search Box
  - Navigation Bar
  - Contact Page
  - Footer
  - Login/Sign-in Option
- Parallel execution with progress spinner
- PDF report generation
- Email report delivery (Gmail)
- Works with both API and Selenium fallback
- Per-site test selection with real-time status

## 🛠 Technologies

- Python (Flask)
- Selenium (Chrome WebDriver)
- Google Custom Search API
- FPDF
- Bootstrap 5

## 🚀 Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
