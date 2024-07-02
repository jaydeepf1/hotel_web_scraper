import time
from utils.config import ConfigBuilder, ConfigReader
from utils.driver import Driver
from utils.generate import Generator
from scraper.hotel_count import HotelCount
from scraper.hotel_search import HotelSearchForm
from scraper.hotel_details_scrapper import HotelScraper
from storage.csv_storage import CSV_storage


def scrape(destination):

    ConfigBuilder().build_config()

    config_reader = ConfigReader()

    destination, dates = config_reader.get_destination_and_dates(
        destination=destination
    )

    cookie_wait = config_reader.get_time("COOKIE_WAIT")

    driver_wait = config_reader.get_time("DRIVER_WAIT")

    url = config_reader.get_URL()

    for check_in_date, check_out_date in dates:

        driver = Driver(url)
        driver = driver.get_driver()

        hotel_search = HotelSearchForm(
            driver,
            driver_wait,
            cookie_wait,
            destination,
            check_in_date,
            check_out_date,
        )

        hotel_search.load_hotels_page()

        hotel_count = HotelCount(driver, driver_wait)
        total_hotels = hotel_count.get_available_hotels_count()
        available_hotels = hotel_count.get_available_hotels_count()

        print(f"Total Hotels : {total_hotels}")
        print(f"Available Hotels : {available_hotels}")

        hotel_scraper = HotelScraper(
            driver,
            driver_wait,
            destination,
            check_in_date,
            check_out_date,
            available_hotels,
        )

        hotel_data = hotel_scraper.get_hotel_data()

        file_name = Generator(
            destination, check_in_date, check_out_date
        ).generate_file_name()

        CSV_storage(destination, hotel_data, file_name).save_to_csv()

        driver.quit()

        time.sleep(3)
