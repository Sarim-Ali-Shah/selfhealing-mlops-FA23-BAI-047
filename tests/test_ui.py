import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.environ.get("BASE_URL", "http://3.106.156.32:32500")

def test_frontend_sentiment():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)
        text_input = wait.until(
            EC.presence_of_element_located((By.ID, "text-input"))
        )
        text_input.send_keys("This movie was absolutely wonderful")
        submit_btn = driver.find_element(By.ID, "submit-btn")
        submit_btn.click()
        wait.until(lambda d: d.find_element(
            By.ID, "result-output").text.strip() != ""
        )
        result_text = driver.find_element(By.ID, "result-output").text
        assert result_text.strip() != ""
        assert any(word in result_text for word in ["POSITIVE", "NEGATIVE", "Confidence"])
    finally:
        driver.quit()