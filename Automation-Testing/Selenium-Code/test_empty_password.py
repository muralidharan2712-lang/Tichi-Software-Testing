from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = "muralikumar2712@gmail.com"
PASSWORD = ""


def test_empty_password(chrome):
    """
    Test: Submitting an empty password field should block login —
    the app should stay on the password step, not navigate away.

    Changes from original:
    - Removed module-level 'driver = webdriver.Chrome()' — chrome fixture used.
    - Removed try/except/finally — exceptions now propagate to pytest.
    - Removed 'import time' and 'time.sleep(5)' — replaced with WebDriverWait
      confirming the password field remains visible after clicking Login,
      meaning the app correctly refused to log in with an empty password.
    - Added assertion: password field (By.ID, "password") must still be displayed.
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

    password_field.send_keys(Keys.TAB)

    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Login']")
        )
    )

    login_btn.click()
    print("Login Clicked")

    # Wait for the password field to remain visible — app should stay on login page
    wait.until(EC.visibility_of_element_located((By.ID, "password")))

    driver.save_screenshot("empty_password.png")
    print("Empty Password Screenshot Saved")

    # Assert: password field still visible — the app correctly blocked empty login
    assert driver.find_element(By.ID, "password").is_displayed(), (
        "Expected the password field to remain visible after submitting an empty "
        "password, indicating the app did not navigate away from the login page."
    )
