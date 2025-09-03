import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    # Keep Chrome open after test (useful for debugging)
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://www.google.com")

    # Handle cookie popup if it appears
    try:
        accept_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Aceptar todo') or contains(., 'Accept all')]")
            )
        )
        accept_btn.click()
    except Exception:
        pass  # no popup → continue

    yield driver
    driver.quit()
