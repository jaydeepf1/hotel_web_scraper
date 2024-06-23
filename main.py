import input_data
from handle_form import search_hotels
from save_to_csv import save_to_csv
from extract_hotel_data import extract_hotel_data
from load_driver import load_driver

if __name__ == '__main__':
    # Load Driver
    driver = load_driver()

    # Input Data
    destinations = input_data.destinations
    check_in_date = input_data.check_in_date
    check_out_date = input_data.check_out_date

    try:
        for destination in destinations:
            # Search Hotels
            search_hotels(driver, destination, check_in_date, check_out_date)

            # Get Hotel Data
            hotel_data = extract_hotel_data(driver, destination, check_in_date,
                                            check_out_date)

            # File Name
            file_name = f'{destinations[0].replace(", ", "_").replace(" ", "_")}_{check_in_date.replace("/", "_")}_To_{check_out_date.replace("/", "_")}.csv'

            # Save Hotel Data
            save_to_csv(hotel_data, filename=file_name)
    finally:
        driver.quit()
