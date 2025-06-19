from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_external_test(url):
    print("Starting Selenium test...")

    options = Options()
    # Comment out headless for now to see browser
    # options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        driver.get(url)

        # Wait for the search box to be present (Google specific)
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        print("Search box found, typing 'usability testing'")
        search_box.send_keys("usability testing")

        # Wait for the Google Search button and click it
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "btnK"))
        )
        search_button.click()

        # Wait for results page to load by checking results div
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        print("Search results loaded successfully")

    except Exception as e:
        print(f"Error during test: {e}")

    finally:
        driver.quit()

    print("Test completed.")

if __name__ == "__main__":
    run_external_test("https://www.google.com")
