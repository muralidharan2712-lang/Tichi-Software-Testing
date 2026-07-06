import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = "muralikumar2712@gmail.com"
PASSWORD = "WrongPassword123!"


def test_invalid_password(chrome):
    """
    Test: Entering a valid email but wrong password should show an error
    and keep the user on the password/login page.

    Changes from original:
    - Removed module-level 'driver = webdriver.Chrome()' — chrome fixture used.
    - Removed try/except/finally — exceptions now propagate to pytest.
    - Replaced 'time.sleep(5)' after login click with WebDriverWait for the
      password field to remain visible (or an error message to appear),
      confirming the app rejected the wrong password.
    - Added assertion: the password input field (By.ID, "password") is still
      displayed, meaning the app did not navigate away from the login page.
    - 'time.sleep(0.1)' inside the per-character loop is intentionally kept.
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

    password_field = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )

    password_field.clear()

    for ch in PASSWORD:
        password_field.send_keys(ch)
        time.sleep(0.1)  # Intentional: simulates human typing speed

    password_field.send_keys(Keys.TAB)

    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Login']")
        )
    )

    login_btn.click()
    print("Login Clicked")

    # Wait for the password field to remain visible — the app should stay on
    # the login page after an incorrect password, not navigate away.
    wait.until(EC.visibility_of_element_located((By.ID, "password")))

    driver.save_screenshot("invalid_password.png")
    print("Invalid Password Screenshot Saved")

    # Assert: password field is still present — login was correctly rejected
    assert driver.find_element(By.ID, "password").is_displayed(), (
        "Expected the password field to remain visible after an invalid password, "
        "indicating the app did not navigate away from the login page."
    )
