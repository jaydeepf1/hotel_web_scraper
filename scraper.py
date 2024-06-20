import csv
import socket
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def enter_destination(driver, destination):
  dest_input = WebDriverWait(driver, 20).until(
      EC.element_to_be_clickable((By.ID, "dest-input")))
  dest_input.send_keys(destination)
  dest_input.send_keys(Keys.RETURN)


def enter_dates(driver, check_in_date, check_out_date):
  check_in_input = WebDriverWait(driver, 20).until(
      EC.element_to_be_clickable((By.ID, "checkInDate")))
  check_in_input.click()
  check_in_input.send_keys(check_in_date)
  check_in_input.send_keys(Keys.RETURN)

  check_out_input = WebDriverWait(driver, 20).until(
      EC.element_to_be_clickable((By.ID, "checkOutDate")))
  check_out_input.click()
  check_out_input.send_keys(check_out_date)
  check_out_input.send_keys(Keys.RETURN)


def perform_search(driver):
  search_button = WebDriverWait(driver, 20).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "search-button")))
  search_button.click()


def accept_cookies(driver):
  try:
    accept_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Accept')]")))
    accept_button.click()
  except Exception:
    pass  # Accept button might not be present, continue without error


def extract_hotel_data(driver, destination, check_in_date, check_out_date):
  hotel_data = []
  hotel_elements = WebDriverWait(driver, 60).until(
      EC.presence_of_all_elements_located(
          (By.XPATH, "//button[contains(text(), 'Select Hotel')]")))

  for index, hotel_button in enumerate(hotel_elements):
    hotel_elements = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//button[contains(text(), 'Select Hotel')]")))
    hotel_button = hotel_elements[index]
    hotel_button.click()
    time.sleep(10)

    wait = WebDriverWait(driver, 20)

    hotel_name_elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//h1[@data-testid="hotel-label"]')))
    room_elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".d-none.d-sm-flex.d-md-flex.roomName")))
    price_elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "span.cash.ng-star-inserted")))

    hotel_name = hotel_name_elements[0].text.strip()
    room_types = [room.text for room in room_elements]
    prices = [price.text for price in price_elements]

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
    time.sleep(5)

  return hotel_data


def find_free_port(start_port=9515, max_ports=10):
  """
    Function to find a free port starting from start_port.
    Returns the first available port found.
    """
  for port in range(start_port, start_port + max_ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      sock.bind(('localhost', port))
      return port
    except OSError:
      continue
    finally:
      sock.close()
  raise RuntimeError("Could not find a free port in the specified range.")


def save_to_csv(data, filename='hotel_data.csv'):
  if data:
    keys = data[0].keys()

    # Write data to CSV file
    with open(filename, 'w', newline='') as output_file:
      dict_writer = csv.DictWriter(output_file, fieldnames=keys)
      dict_writer.writeheader()
      dict_writer.writerows(data)

    print(f"Data saved to {filename}")
  else:
    print("No data to save")


def fetch_hotel_data(destination, check_in_date, check_out_date, driver):
  retries = 3  # Number of retries
  for attempt in range(retries):
    try:
      driver.maximize_window()
      driver.get('https://www.ihg.com/hotels/us/en/reservation')

      enter_destination(driver, destination)
      enter_dates(driver, check_in_date, check_out_date)
      perform_search(driver)
      time.sleep(10)
      accept_cookies(driver)

      hotel_data = extract_hotel_data(driver, destination, check_in_date,
                                      check_out_date)
      return hotel_data

    except Exception as e:
      print(f"Attempt {attempt+1} failed. Error: {e}")
      if attempt < retries - 1:
        print("Retrying...")
        continue
      else:
        print("All attempts failed. Returning empty list.")
        return []


def main():
  # Define the destinations and dates
  destinations = [
      'Chattanooga, TN, United States',
      'Chattanooga Lovell Airport, TN, United States'
  ]
  check_in_date = datetime(2024, 5, 20).strftime('%m/%d/%Y')
  check_out_date = datetime(2024, 5, 30).strftime('%m/%d/%Y')

  # Find a free port dynamically
  try:
    chrome_driver_port = find_free_port()
    print(f"Using ChromeDriver port: {chrome_driver_port}")
  except RuntimeError as e:
    print(f"Error finding a free port: {e}")
    exit(1)

  # Suppress Selenium logging
  options = Options()
  options.add_argument("--log-level=3")  # Suppress most logs
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--disable-gpu")
  options.add_argument("--disable-software-rasterizer")
  options.add_argument("--disable-extensions")
  options.add_argument("--headless=new")  # Enable new headless mode
  options.add_argument("start-maximized")
  options.add_argument("disable-infobars")
  options.add_argument("--disable-extensions")
  options.add_argument("--disable-gpu")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--no-sandbox")
  options.add_argument(
      "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  )

  # Initialize ChromeDriver with the dynamically found port
  # service = Service(port=chrome_driver_port)
  driver = webdriver.Chrome(options=options)

  try:
    for destination in destinations:
      hotel_data = fetch_hotel_data(destination, check_in_date, check_out_date,
                                    driver)
      file_name = f'{destination.replace(", ", "_").replace(" ", "_")}_{check_in_date.replace("/", "_")}_To_{check_out_date.replace("/", "_")}.csv'
      save_to_csv(hotel_data, filename=file_name)
      time.sleep(15)
  finally:
    driver.quit()


if __name__ == '__main__':
  main()
