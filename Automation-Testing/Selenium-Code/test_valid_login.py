import time


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = "muralikumar2712@gmail.com"
PASSWORD = "!@27Murali2005"


def test_valid_login(chrome):
    """
    Test: Successful login with valid credentials.

    Changes from original:
    - Removed module-level 'driver = webdriver.Chrome()' — the 'chrome' fixture
      from conftest.py provides the driver and handles teardown via yield.
    - Removed try/except/finally — exceptions now propagate so pytest can
      correctly report FAIL. The fixture's yield guarantees driver.quit().
    - Replaced 'time.sleep(5)' after login click with WebDriverWait for a
      post-login element (the dashboard URL change). Fixed sleeps are unreliable
      and slow; waiting for an actual condition is deterministic.
    - Added assertion: verifies the URL no longer contains '/login', confirming
      that login succeeded and the app navigated to the dashboard.
    - 'time.sleep(0.1)' inside the per-character loop is intentionally kept —
      it simulates realistic human typing speed and is not an arbitrary wait.
    """
    driver = chrome
    wait = WebDriverWait(driver, 30)  # 30s to allow post-login redirect

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

    password = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )

    password.clear()

    for ch in PASSWORD:
        password.send_keys(ch)
        time.sleep(0.1)  # Intentional: simulates human typing speed

    password.send_keys(Keys.TAB)

    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Login']")
        )
    )

    login_btn.click()
    print("Login Clicked")

    # Wait until the URL changes away FROM the /login page.
    # Previously used the root URL as the reference — that was already "changed"
    # the moment we were on /login, so the wait returned True immediately.
    # Now we pass the exact current login URL so WebDriverWait actually blocks
    # until the redirect to the dashboard happens.
    wait.until(EC.url_changes("https://tichi-app-webapp-stage.web.app/login"))

    driver.save_screenshot("valid_login_success.png")
    print("Dashboard Screenshot Saved")

    # Assert: login redirected away from the auth/login screen
    assert "login" not in driver.current_url.lower(), (
        f"Expected to leave the login page after valid login, "
        f"but current URL is: {driver.current_url}"
    )
