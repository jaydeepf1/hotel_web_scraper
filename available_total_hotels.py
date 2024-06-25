import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from logger import set_log

# Initialize the custom logger
logger = set_log()


def available_total_hotels(destination, driver):
    """
    Get the total number of available hotels shown on the IHG website.

    Args:
    - driver: WebDriver instance.

    Returns:
    - int: Total number of available hotels (or 0 if not found).
    """
    try:
        scroll_amount = driver.execute_script(
            "return document.documentElement.scrollHeight") / 2
        driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
        time.sleep(3)  # Adjust the sleep time if necessary

        hotel_elements = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[contains(text(), 'Select Hotel')]")))
        hotel_count = len(hotel_elements)

        logger.info(f'{destination} First scroll: {hotel_count}')

        scroll_amount = driver.execute_script(
            "return document.documentElement.scrollHeight") / 2
        driver.execute_script(
            f"window.scrollTo({scroll_amount}, {2 * scroll_amount});")
        time.sleep(3)  # Adjust the sleep time if necessary

        hotel_elements = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[contains(text(), 'Select Hotel')]")))
        hotel_count = max(hotel_count, len(hotel_elements))

        logger.info(
            f'{destination} Total Number of Available Hotels: {hotel_count}')
        return hotel_count

    except Exception as e:
        logger.error(
            f"{destination} Error retrieving available hotel count: {str(e)}")
        return 0
