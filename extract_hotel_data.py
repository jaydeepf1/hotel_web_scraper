import time
from get_total_hotels import get_total_hotels
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def extract_hotel_data(driver, destination, check_in_date, check_out_date):
    total_num_hotels = get_total_hotels(driver)
    hotel_data = []    
    for index in range(total_num_hotels):
        print(f'Hotel Number : {index+1}')
        try:
            hotel_elements = WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Select Hotel')]"))
            )
            hotel_elements[index].click()
            time.sleep(3)
        except Exception as e:
            print(e)
            return hotel_data

        wait = WebDriverWait(driver, 10)
        
        hotel_name_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="hotel-label"]'))
        )
        room_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".d-none.d-sm-flex.d-md-flex.roomName"))
        )
        price_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.cash.ng-star-inserted"))
        )

        hotel_name = hotel_name_element.text.strip()
        room_types = [room.text for room in room_elements]
        prices = [price.text for price in price_elements]

        print(hotel_name)

        for room_type, price in zip(room_types, prices):
            hotel_data.append({
                'Location': destination,
                'Check-in Date': check_in_date,
                'Check-out Date': check_out_date,
                'Hotel Name': hotel_name,
                'Room Type': room_type,
                'Price (INR)': price
            })

        driver.back()
        time.sleep(3)

    return hotel_data