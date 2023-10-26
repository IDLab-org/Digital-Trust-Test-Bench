import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(scope='module')
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
        
    with webdriver.Chrome(options=options) as driver:
        yield driver

def verify_element_text(driver, xpath, expected_text, error_message):
    element = driver.find_element(By.XPATH, xpath)
    assert element is not None, f"Element with xpath {xpath} is not found"
    assert expected_text in element.text, error_message
