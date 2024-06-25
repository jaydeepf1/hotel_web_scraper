from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger import set_log

# Initialize the custom logger
logger = set_log()


def get_total_hotels(destination, driver):
    """
    Get the total number of hotels found on the IHG website.

    Args:
    - driver: WebDriver instance.

    Returns:
    - int: Total number of hotels found (or 0 if not found).
    """
    try:
        # Wait for the element to be visible (adjust timeout as needed)
        element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'rooms-count')))

        # Extract the text content containing the number of hotels found
        hotel_count_text = element.text

        # Parse the number of hotels found from the text
        # Assuming the format is "X Hotels Found"
        hotel_count = int(
            hotel_count_text.split()
            [0])  # Extract the number part and convert to integer

        logger.info(f'{destination} Total Number of Hotels: {hotel_count}')
        return hotel_count

    except Exception as e:
        logger.error(
            f'{destination} Failed to retrieve total hotel count: {str(e)}')
        return 0
