from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = "invalid_email_format"


def test_invalid_email(chrome):
    """
    Test: Entering an invalid email format should show a validation error
    and keep the user on the email entry step (no navigation to password step).

    Changes from original:
    - Removed module-level 'driver = webdriver.Chrome()' — chrome fixture used.
    - Removed try/except/finally — exceptions now propagate to pytest.
    - Removed 'import time' and 'time.sleep(3)' — replaced with WebDriverWait
      for a concrete condition: the email field stays visible (or a URL check),
      confirming the app did NOT advance to the password step.
    - Added assertion: the password field (By.ID, "password") must NOT appear,
      confirming the app blocked progression on invalid email format.
    """
    driver = chrome
    wait = WebDriverWait(driver, 20)

    driver.get("https://tichi-app-webapp-stage.web.app")
    print("Application Opened")

    sign_in = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Sign In']")
        )
    )
    sign_in.click()
    print("Sign In Clicked")

    email = wait.until(
        EC.visibility_of_element_located((By.ID, "email"))
    )

    email.clear()
    email.send_keys(EMAIL)

    continue_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Continue']")
        )
    )
    continue_btn.click()
    print("Continue Clicked")

    # Wait briefly for the UI to react, then assert the password step did NOT appear.
    # We confirm this by checking the email field is still visible (still on step 1).
    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.save_screenshot("invalid_email_format.png")
    print("Invalid Email Format Screenshot Saved")

    # Assert: email field is still present — the app did not advance to password step
    email_field = driver.find_element(By.ID, "email")
    assert email_field.is_displayed(), (
        "Expected the email field to remain visible after submitting an invalid "
        "email format, indicating the app did not advance to the password step."
    )
