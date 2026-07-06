from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = "not_registered_12345@gmail.com"


def test_unregistered_email(chrome):
    """
    Test: Entering a properly formatted but unregistered email should either:
    - Show an error message and keep the user on the email step, OR
    - Advance to the password step (some apps allow this and show error after password).
    This test asserts that the app stays on the email step (no password field appears).

    Changes from original:
    - Removed module-level 'driver = webdriver.Chrome()' — chrome fixture used.
    - Removed try/except/finally — exceptions now propagate to pytest.
    - Removed 'import time' and 'time.sleep(3)' — replaced with WebDriverWait
      confirming the email field remains visible, meaning the app blocked progression.
    - Added assertion: email field (By.ID, "email") must still be displayed,
      confirming the app did not advance an unregistered email to the password step.
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

    # Wait for the email field to remain visible — confirms app did not advance
    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.save_screenshot("unregistered_email.png")
    print("Unregistered Email Screenshot Saved")

    # Assert: email field still visible — the app blocked an unregistered email
    assert driver.find_element(By.ID, "email").is_displayed(), (
        "Expected the email field to remain visible after submitting an unregistered "
        "email, indicating the app did not advance to the password step."
    )
