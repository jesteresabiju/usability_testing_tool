# app.py
import os, datetime, smtplib, re, requests
from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fpdf import FPDF
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from PyPDF2 import PdfMerger

from dotenv import load_dotenv

load_dotenv()  # loads from .env file

app = Flask(__name__)
IS_DEPLOYED = os.environ.get('DEPLOYED', 'false').lower() == 'true'
app.secret_key = 'supersecretkey'

PDF_DIR = 'pdf_reports'
os.makedirs(PDF_DIR, exist_ok=True)

EMAIL_ADDRESS = 'workwithjesse123@gmail.com'
EMAIL_PASSWORD = 'gyvn cmso hyjh lgsn'
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = '628713b1419ca4292'

HEADLESS_MODE = True
progress = {'current': 0, 'total': 0, 'done': True}

def validate_url(url):
    return re.match(r"^(http(s)?://)?([\w-]+\.)+[\w-]{2,4}", url)

def get_driver(headless=True):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("user-agent=Mozilla/5.0")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def detect_api(url, query):
    try:
        domain = urlparse('http://' + url if not url.startswith(('http://', 'https://')) else url).netloc
        domain = domain.replace('www.', '')
        res = requests.get(f"https://www.googleapis.com/customsearch/v1?q=site:{domain}+{query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}")
        data = res.json()
        print("API RESPONSE:", data)

        if 'items' not in data:
            return 'FAIL'

        keywords = {
            'search': ['search', 'find', 'query'],
            'contact': ['contact', 'email', 'phone'],
            'login': ['login', 'sign in', 'signin', 'account']
        }
        match_keywords = keywords.get(query.lower(), [])
        for item in data['items']:
            text = (item.get('title', '') + item.get('snippet', '')).lower()
            if any(k in text for k in match_keywords):
                return 'PASS'
        return 'FAIL'
    except Exception as e:
        print(f"[API] ERROR: {e}")
        return 'FAIL'

def detect_element_selenium(url, selectors):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    try:
        driver = get_driver(HEADLESS_MODE)
        driver.get(url if url.startswith('http') else f"http://{url}")

        for sel in selectors:
            try:
                WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
                print(f"[SEL] ✅ Found selector: {sel} on {url}")
                driver.quit()
                return 'PASS'
            except TimeoutException:
                print(f"[SEL] ❌ Timeout for selector: {sel} on {url}")
                continue

        print(f"[SEL] ❌ None of the selectors matched on {url}")
        driver.quit()
        return 'FAIL'
    except Exception as e:
        print(f"[SEL] ❌ Error loading {url}: {str(e)}")
        try:
            driver.quit()
        except:
            pass
        return 'FAIL'

def detect_search(url):
    result = detect_api(url, "search")
    return result if result == 'PASS' else detect_element_selenium(url, [
        "input[type='search']",
        "input[name*='search']",
        "input[id*='search']",
        "input[class*='search']",
        "form[role='search'] input[type='text']",
        "input[placeholder*='search']",
        "input[aria-label*='search']",
        "input[type='text'][name*='q']",
        "form input[type='text']"
    ])

def detect_navbar(url):
    return detect_element_selenium(url, [
        "nav",
        "header nav",
        "div[class*='nav']",
        "div[id*='nav']",
        ".navbar",
        "#navbar",
        "ul.nav",
        "header ul",
        ".menu",
        "#menu",
        "#mainnav",
        "#p-navigation",           # Wikipedia-specific
        "#mw-head",                # Wikipedia header
        "#mw-panel",              # Sidebar menu container on Wikipedia
        "div#left-navigation"     # Another Wikipedia region
    ])

def detect_contact(url):
    result = detect_api(url, "contact")
    return result if result == 'PASS' else detect_element_selenium(url, [
        "a[href*='contact']",
        "footer a[href*='contact']",
        "nav a[href*='contact']",
        "a[title*='contact']"
    ])

def detect_footer(url):
    return detect_element_selenium(url, [
        "footer",
        "#footer",
        ".footer",
        "div[class*='footer']",
        "section[class*='footer']",
        "div[id*='footer']",
        "#copyright",
        "#footer-places",         # Wikipedia bottom links
        "#footer-icons",          # Icon region in footer
        "#f-list",                # Footer navigation links list
        "#footer-info"            # Wikipedia info block in footer
    ])

def detect_login(url):
    result = detect_api(url, "login")
    return result if result == 'PASS' else detect_element_selenium(url, [
        "input[type='password']",
        "a[href*='login']",
        "a[href*='signin']",
        "a[href*='sign-in']",
        "a[href*='account']",
        "button[class*='login']",
        "button[id*='login']",
        "button[name*='login']",
        "input[name*='username'] + input[type='password']",
        "form[action*='login']"
    ])

def run_test(test):
    result = {'name': test['name'], 'url': test['url'], 'selected': test['selected']}
    if 'search' in test['selected']: result['search'] = detect_search(test['url'])
    if 'navbar' in test['selected']: result['navbar'] = detect_navbar(test['url'])
    if 'contact' in test['selected']: result['contact'] = detect_contact(test['url'])
    if 'footer' in test['selected']: result['footer'] = detect_footer(test['url'])
    if 'login' in test['selected']: result['login'] = detect_login(test['url'])
    return result

def generate_pdf(results, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Usability Test Report", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    col_widths = {'Test Name': 40, 'URL': 50, 'Search': 20, 'Navbar': 20, 'Contact': 22, 'Footer': 22, 'Login': 22}
    pdf.set_font("Arial", 'B', 10)
    for header in col_widths:
        pdf.cell(col_widths[header], 10, header, 1, align='C')
    pdf.ln()

    pdf.set_font("Arial", '', 9)
    for r in results:
        pdf.cell(col_widths['Test Name'], 10, r.get('name', '')[:30], 1)
        pdf.cell(col_widths['URL'], 10, r.get('url', '')[:40], 1)
        for k in ['search', 'navbar', 'contact', 'footer', 'login']:
            pdf.cell(col_widths[k.capitalize()], 10, r.get(k, 'N/A'), 1, align='C')
        pdf.ln()

    path = os.path.join(PDF_DIR, filename)
    pdf.output(path)
    return path

@app.route('/')
def home():
    return render_template('index.html', deployed=IS_DEPLOYED)

@app.route('/test_external', methods=['GET', 'POST'])
def test_external():
    if request.method == 'POST':
        urls = request.form.getlist('urls')
        names = request.form.getlist('names')
        all_tests = request.form.getlist('tests')

        tests = []
        for i in range(len(urls)):
            selected = request.form.getlist(f'tests_{i}')
            if not selected:
                selected = ['search', 'navbar', 'contact', 'footer', 'login']
            tests.append({'url': urls[i].strip(), 'name': names[i].strip(), 'selected': selected})

        session['progress'] = {'total': len(tests), 'current': 0}
        progress['total'] = len(tests)
        progress['current'] = 0
        progress['done'] = False

        results = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(run_test, test) for test in tests]
            for future in futures:
                results.append(future.result())
                progress['current'] += 1

        progress['done'] = True
        session['current_tests'] = results
        filename = f"report_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_path = generate_pdf(results, filename)
        session['results'] = results

        if os.path.exists(pdf_path):
            session['current_pdfs'] = session.get('current_pdfs', []) + [pdf_path]
        else:
            flash(f"PDF report could not be generated for {filename}", "danger")
            session['current_pdfs'] = session.get('current_pdfs', [])


        if len(session['current_pdfs']) > 1:
           merger = PdfMerger()
           valid_paths = [p for p in session['current_pdfs'] if os.path.exists(p)]
           for path in valid_paths:
               merger.append(path)
           all_path = f"{PDF_DIR}/all_reports.pdf"
           merger.write(all_path)
           merger.close()
           session['all_pdf'] = all_path
        elif session['current_pdfs']:
           session['all_pdf'] = session['current_pdfs'][-1]
        else:
           session['all_pdf'] = None


        session.modified = True
        return redirect(url_for('results'))

    return render_template('test_external.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email import encoders
        import ssl

        email = request.form.get('email')
        choice = request.form.get('choice')
        filepath = session.get('all_pdf') if choice == 'all' else session.get('current_pdfs', [None])[-1]

        if not filepath or not os.path.exists(filepath):
            flash("Report file not found", "danger")
            return redirect(url_for('results'))

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = 'Usability Test Report'
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(filepath, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filepath)}')
        msg.attach(part)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
            flash("Email sent successfully!", "success")
        except Exception as e:
            flash("Failed to send email", "danger")

    return render_template('test_external_confirm.html',
        tests=session.get('current_tests', []),
        last_pdf=session.get('current_pdfs', [None])[-1],
        all_pdf=session.get('all_pdf'))

@app.route('/status')
def status():
    return jsonify(progress)

@app.route('/download_current')
def download_current():
    return send_file(session.get('current_pdfs', [None])[-1], as_attachment=True)

@app.route('/download_all')
def download_all():
    return send_file(session.get('all_pdf'), as_attachment=True)

@app.route('/clear', methods=['POST'])
def clear():
    session.clear()
    flash("Session cleared", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)