import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger import set_log

# Initialize the custom logger
logger = set_log()

def enter_destination(driver, destination):
    """
    Enter destination in the input field on the IHG website.
    
    Args:
    - driver: WebDriver instance.
    - destination: Destination string.
    """
    dest_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "dest-input"))
    )
    dest_input.send_keys(destination)
    dest_input.send_keys(Keys.RETURN)

def enter_dates(driver, check_in_date, check_out_date):
    """
    Enter check-in and check-out dates on the IHG website.
    
    Args:
    - driver: WebDriver instance.
    - check_in_date: Check-in date string.
    - check_out_date: Check-out date string.
    """
    check_in_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "checkInDate"))
    )
    check_in_input.click()
    check_in_input.send_keys(check_in_date)
    check_in_input.send_keys(Keys.RETURN)

    check_out_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "checkOutDate"))
    )
    check_out_input.click()
    check_out_input.send_keys(check_out_date)
    check_out_input.send_keys(Keys.RETURN)

def perform_search(driver):
    """
    Click the search button on the IHG website.
    
    Args:
    - driver: WebDriver instance.
    """
    search_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "search-button"))
    )
    search_button.click()

def accept_cookies(driver):
    """
    Click the accept cookies button if present on the IHG website.
    
    Args:
    - driver: WebDriver instance.
    """
    try:
        accept_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Accept')]"))
        )
        accept_button.click()
    except Exception:
        pass  # Accept button might not be present, continue without error

def select_currency(driver, currency="USD"):
    """
    Select currency from the dropdown on the IHG website.
    
    Args:
    - driver: WebDriver instance.
    - currency: Currency code (default is USD).
    """
    try:
        dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "app-currency-selector .ng-tns-c2569113336-7.ui-dropdown"))
        )
        dropdown.click()

        dropdown_wrapper = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ui-dropdown-items-wrapper"))
        )

        currency_options = dropdown_wrapper.find_elements(By.XPATH, "//li[@role='option']")
        
        for option in currency_options:
            if option.text.strip() == currency:
                option.click()
                break
    except Exception:
        pass

def search_hotels(driver, destination, check_in_date, check_out_date):
    """
    Perform hotel search on the IHG website.
    
    Args:
    - driver: WebDriver instance.
    - destination: Destination string.
    - check_in_date: Check-in date string.
    - check_out_date: Check-out date string.
    """
    try:
        driver.maximize_window()
        driver.get('https://www.ihg.com/hotels/us/en/reservation')
        enter_destination(driver, destination)
        enter_dates(driver, check_in_date, check_out_date)
        perform_search(driver)
        time.sleep(10)  # Adjust as needed based on page load time
        select_currency(driver)
        accept_cookies(driver)
    except Exception as e:
        error_msg = f"Error occurred while searching hotels: {str(e)}"
        logger.error(error_msg)  # Use the custom logger
        # Handle the exception as per your requirement
