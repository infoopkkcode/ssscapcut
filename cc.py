from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

def get_download_link(link, url="https://ssscap.net/"):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        # Set up Chrome options for headless mode and disabling images
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        prefs = {"profile.managed_default_content_settings.images": 2}  # Disable images
        chrome_options.add_experimental_option("prefs", prefs)

        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        logging.info("Chrome WebDriver initialized successfully.")

        # Navigate to the specified URL
        driver.get(url)
        logging.info(f"Navigated to URL: {url}")

        # Handle consent message
        try:
            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-button.fc-cta-consent.fc-primary-button"))
            )
            consent_button.click()
            logging.info("Consent button clicked.")
        except Exception as e:
            logging.warning(f"Consent button not found or could not be clicked: {e}")

        # Find the input element and enter the link
        link_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'text_input')))
        logging.info("Input element found.")
        # Take a screenshot before interacting with the element
        link_input.clear()
        link_input.send_keys(link)
        link_input.send_keys(Keys.RETURN)
        logging.info("Link submitted.")

        # Find the download link element and return its href attribute
        download_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.download_link')))
        logging.info("Download link found.")
        return download_link.get_attribute('href')
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()
            logging.info("Browser closed.")

# Example Usage
if __name__ == "__main__":
    result = get_download_link("https://example.com")
    print(f"Download link: {result}")
