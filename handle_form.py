import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def enter_destination(driver, destination):
    dest_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "dest-input"))
    )
    dest_input.send_keys(destination)
    dest_input.send_keys(Keys.RETURN)

def enter_dates(driver, check_in_date, check_out_date):
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
    search_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "search-button"))
    )
    search_button.click()

def accept_cookies(driver):
    try:
        accept_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Accept')]"))
        )
        accept_button.click()
    except Exception:
        pass  # Accept button might not be present, continue without error

def search_hotels(driver, destination, check_in_date, check_out_date):
    driver.maximize_window()
    driver.get('https://www.ihg.com/hotels/us/en/reservation')
    enter_destination(driver, destination)
    enter_dates(driver, check_in_date, check_out_date)
    perform_search(driver)
    time.sleep(10)
    accept_cookies(driver)