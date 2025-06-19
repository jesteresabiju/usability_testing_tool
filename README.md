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


