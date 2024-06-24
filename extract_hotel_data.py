import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from get_total_hotels import get_total_hotels
from available_total_hotels import available_total_hotels
from logger import set_log

# Initialize the custom logger
logger = set_log()

def extract_hotel_data(driver, destination, check_in_date, check_out_date):
    """
    Extract hotel data from the IHG website for a given destination and date range.
    
    Args:
    - driver: WebDriver instance.
    - destination (str): Destination name.
    - check_in_date (str): Check-in date.
    - check_out_date (str): Check-out date.
    
    Returns:
    - list: List of dictionaries containing hotel data.
    """
    try:
        get_total_hotels(driver)
        total_num_hotels = available_total_hotels(driver)
        hotel_data = []
        scroll_amount = 0
        driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
        
        for index in range(total_num_hotels):
            logger.info(f'Hotel Number : {index+1}')
            
            try:
                if index >= 9:
                    scroll_amount = driver.execute_script(
                        "return document.documentElement.scrollHeight") / 2
                    driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
                    time.sleep(3)
                
                hotel_elements = WebDriverWait(driver, 60).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//button[contains(text(), 'Select Hotel')]")))
                hotel_elements[index].click()
                time.sleep(3)
            
            except Exception as e:
                logger.error(f"Error clicking hotel element: {str(e)}")
                logger.info(f'Save {index} hotel out of {total_num_hotels}.')
                return hotel_data
            
            try:
                wait = WebDriverWait(driver, 60)
                hotel_name_element = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//h1[@data-testid="hotel-label"]')))
                room_elements = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ".d-none.d-sm-flex.d-md-flex.roomName")))
                price_elements = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "span.cash.ng-star-inserted")))

                hotel_name = hotel_name_element.text.strip()
                room_types = [room.text for room in room_elements]
                prices = [price.text for price in price_elements]

                logger.info(f'Extracting data for hotel: {hotel_name}')

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
                logger.error(f"Error extracting data: {str(e)}")
                logger.info(f'Save {index} hotel out of {total_num_hotels}.')
                return hotel_data
            
            finally:
                driver.back()
                time.sleep(3)

        logger.info(f'Saved {total_num_hotels} hotels out of {total_num_hotels}.')
        return hotel_data
    
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return []
