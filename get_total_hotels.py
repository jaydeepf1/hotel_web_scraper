import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_total_hotels(driver):
  # Wait for the element containing the total number of hotels to be present
  total_hotels_element = WebDriverWait(driver, 60).until(
      EC.presence_of_element_located(
          (By.XPATH,
           "//div[@role='alert' and contains(@class, 'd-none d-sm-block')]")))

  # Extract the text from the element
  total_hotels_text = total_hotels_element.text

  # Use regex to find the number in the text
  match = re.search(r"(\d+) Hotels Found", total_hotels_text)
  if match:
    total_hotels = int(match.group(1))
    print(f'Total Hotels : {total_hotels}')
    return total_hotels
  else:
    print('Total hotels not found in the text')
    return 0