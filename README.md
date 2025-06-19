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

usability_testing_tool/
├── app.py # Main Flask app
├── external_test_runner.py # Background test logic
├── test_app.py # Unit test module
├── utils/ # Utility functions (e.g., API, Selenium)
├── templates/ # HTML templates (Jinja2)
├── static/ # CSS, JS, spinner, report placeholder
├── pdf_reports/ # (Ignored) generated PDF reports
├── data/ # Email + API config if needed
├── tests/ # (Optional) for test scripts
├── requirements.txt
├── tasks.json
├── Procfile
├── .gitignore
└── README.md

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/jesteresabiju/usability_testing_tool.git
cd usability_testing_tool
2. Install Dependencies
Make sure you're using Python 3.8+ and then run:

bash
Copy
Edit
pip install -r requirements.txt
3. Run the App
bash
Copy
Edit
python app.py
Visit the app in your browser at:
http://localhost:5000

🔐 Configuration
Create a config.py or use environment variables for:

python
Copy
Edit
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'
GOOGLE_API_KEY = 'your_google_api_key'
SEARCH_ENGINE_ID = 'your_cse_id'
For Gmail, generate an App Password if 2FA is enabled.

📤 Deployment
This app is deployable on platforms like Heroku, Render, or Railway.

Make sure to:

Set environment variables for email + API keys

Use the provided Procfile for deployment

Install Chrome & chromedriver (if using Selenium in headless mode)

📜 License
This project is licensed under the MIT License.

👤 Author
Developed by @jesteresabiju

📬 Contact
For questions or support, email: workwithjesse123@gmail.com
