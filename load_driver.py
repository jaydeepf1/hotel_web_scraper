import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from logger import set_log

# Initialize the custom logger
logger = set_log()


def load_options():
    """
    Configure Chrome options for WebDriver.
    """
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    )
    options.add_argument(
        "--headless=new")  # Uncomment this line if running headless

    return options


def find_free_port():
    """
    Try to find a free port from a predefined list.
    """
    chrome_driver_port = random.choice(
        [7000, 8005, 9010, 1000, 2005, 3010, 4000, 5005, 6010, 1010])
    logger.info(f"Using port: {chrome_driver_port}")
    return chrome_driver_port  # Return the port if successfully chosen


def initialize_driver():
    """
    Initialize Chrome WebDriver with configured options and service.
    """
    options = load_options()

    retry_count = 5

    for attempt in range(1, retry_count + 1):
        try:
            service = Service(port=find_free_port())
            driver = webdriver.Chrome(service=service, options=options)
            return driver  # If successful, return the driver
        except Exception as e:
            logger.error(
                f"Error initializing Chrome WebDriver (attempt {attempt}): {e}"
            )
            if attempt == retry_count:
                logger.error(
                    "Failed to initialize Chrome WebDriver after multiple attempts."
                )
                raise SystemExit(1)
            time.sleep(1)  # Wait before retrying


def load_driver():
    driver = initialize_driver()
    return driver
