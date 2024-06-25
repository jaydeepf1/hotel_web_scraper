import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from get_total_hotels import get_total_hotels
from available_total_hotels import available_total_hotels
from logger import set_log

# Initialize the custom logger
logger = set_log()


# Retry mechanism for clicking elements
def retry_click(element):
    for _ in range(3):  # Retry up to 3 times
        try:
            element.click()
            return True
        except TimeoutException:
            continue
    return False


# Function to wait for element presence
def wait_for_element(driver, locator, timeout=60):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator))


# Function to wait for all elements presence
def wait_for_elements(driver, locator, timeout=60):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located(locator))


# Function to handle errors and logging
def handle_error(logger, message, index, total_num_hotels, hotel_data):
    logger.error(message)
    logger.info(f'Save {index} hotel out of {total_num_hotels}.')
    return hotel_data


def scroll_to(driver, scroll_amount):
    driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
    time.sleep(3)  # Adjust sleep time based on page responsiveness


def extract_hotel_data(driver, destination, check_in_date, check_out_date):
    try:
        get_total_hotels(destination, driver)
        total_num_hotels = available_total_hotels(destination, driver)
        hotel_data = []
        scroll_amount = 0
        driver.execute_script(f"window.scrollTo(0, {scroll_amount});")

        for index in range(total_num_hotels):
            logger.info(f'{destination} Hotel Number : {index+1}')

            try:
                if index >= 9:
                    scroll_amount = driver.execute_script(
                        "return document.documentElement.scrollHeight") / 1.4
                    scroll_to(driver, scroll_amount)

                hotel_elements = wait_for_elements(
                    driver,
                    (By.XPATH, "//button[contains(text(), 'Select Hotel')]"))

                if not retry_click(hotel_elements[index]):
                    return handle_error(
                        logger, "Failed to click hotel element after retries.",
                        index, total_num_hotels, hotel_data)

                time.sleep(3)  # Add a small delay after clicking

            except TimeoutException:
                return handle_error(
                    logger, f"{destination} Timed out clicking hotel element.",
                    index, total_num_hotels, hotel_data)
            except Exception as e:
                return handle_error(
                    logger,
                    f"{destination} Error clicking hotel element: {str(e)}",
                    index, total_num_hotels, hotel_data)

            try:
                hotel_name_element = wait_for_element(
                    driver, (By.XPATH, '//h1[@data-testid="hotel-label"]'))
                room_elements = wait_for_elements(
                    driver,
                    (By.CSS_SELECTOR, ".d-none.d-sm-flex.d-md-flex.roomName"))
                price_elements = wait_for_elements(
                    driver, (By.CSS_SELECTOR, "span.cash.ng-star-inserted"))

                hotel_name = hotel_name_element.text.strip()
                room_types = [room.text for room in room_elements]
                prices = [price.text for price in price_elements]

                logger.info(
                    f'{destination} Extracting data for hotel: {hotel_name}')

                for room_type, price in zip(room_types, prices):
                    hotel_data.append({
                        'Location': destination,
                        'Check-in Date': check_in_date,
                        'Check-out Date': check_out_date,
                        'Hotel Name': hotel_name,
                        'Room Type': room_type,
                        'Price (USD)': price
                    })

            except Exception as e:
                return handle_error(
                    logger, f"{destination} Error extracting data: {str(e)}",
                    index, total_num_hotels, hotel_data)

            finally:
                driver.back()
                time.sleep(3)

        logger.info(
            f'Saved {total_num_hotels} hotels out of {total_num_hotels}. {destination}'
        )
        return hotel_data

    except Exception as e:
        logger.error(f"{destination} Exception occurred: {str(e)}")
        return []
