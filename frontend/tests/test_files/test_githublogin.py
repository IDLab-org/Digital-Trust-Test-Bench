import pytest
from selenium.webdriver.common.by import By
from test_utilities import driver, verify_element_text

TEST_URL = "http://dtt-dev.internal.idlab.org:5000/auth/login"
GITHUB_LOGIN_XPATH = "//a[@href='/auth/github_login']"
EXPECTED_GITHUB_URL = "https://github.com/login"


def test_page_load(driver):
    driver.get(TEST_URL)
    assert "Login" in driver.page_source, "Login text is not present in the form"


def test_github_login_form(driver):
    driver.get(TEST_URL)

    # Verify the Login with GitHub button
    verify_element_text(
        driver,
        GITHUB_LOGIN_XPATH,
        "with GitHub",
        "Login with GitHub text is not present in the button",
    )

    # Interact and verify URL
    github_login_button = driver.find_element(By.XPATH, GITHUB_LOGIN_XPATH)
    github_login_button.click()
    driver.implicitly_wait(5)
    assert driver.current_url.startswith(EXPECTED_GITHUB_URL)
