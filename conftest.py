import os
import pytest
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup options for headless mode
def pytest_setup_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return options

# Configure driver path
def pytest_configure():
    try:
        driver_path = ChromeDriverManager().install()
        os.environ["PATH"] += os.pathsep + os.path.dirname(driver_path)
        print(f"ChromeDriver installed at: {driver_path}")
    except Exception as e:
        print(f"Failed to install ChromeDriver: {e}")
