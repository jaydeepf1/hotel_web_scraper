import time
from input_data import destinations, check_in_date, check_out_date
from handle_form import search_hotels
from save_to_csv import save_to_csv
from extract_hotel_data import extract_hotel_data
from load_driver import load_driver
from logger import set_log

# Initialize the custom logger
logger = set_log()


def process_destination(driver, destination, check_in_date, check_out_date):
    """
    Process each destination to search hotels, extract data, and save to CSV.
    
    Args:
    - driver: WebDriver instance for scraping.
    - destination: Destination name.
    - check_in_date: Check-in date.
    - check_out_date: Check-out date.
    """
    try:
        # Search Hotels
        search_hotels(driver, destination, check_in_date, check_out_date)

        # Get Hotel Data
        hotel_data = extract_hotel_data(driver, destination, check_in_date,
                                        check_out_date)

        # File Name
        file_name = generate_file_name(destination, check_in_date,
                                       check_out_date)

        # Save Hotel Data
        save_to_csv(hotel_data, filename=file_name)

        time.sleep(30)  # Wait before the next iteration

    except Exception as e:
        error_msg = f"Exception occurred for {destination}: {str(e)}"
        logger.error(error_msg)  # Use the custom logger
        # Handle the exception as per your requirement

    finally:
        driver.quit()  # Quit the driver after processing each destination
        time.sleep(30)


def generate_file_name(destination, check_in_date, check_out_date):
    """
    Generate a CSV file name based on destination and dates.
    
    Args:
    - destination: Destination name.
    - check_in_date: Check-in date.
    - check_out_date: Check-out date.
    
    Returns:
    - str: Generated file name.
    """
    formatted_destination = destination.replace(", ", "_").replace(" ", "_")
    formatted_check_in = check_in_date.replace("/", "_")
    formatted_check_out = check_out_date.replace("/", "_")
    return f'{formatted_destination}_{formatted_check_in}_To_{formatted_check_out}.csv'


def main():
    """
    Main function to iterate over destinations and process each one.
    """
    start_time = time.time()  # Start the timer

    try:
        for destination in destinations:
            # Load fresh driver for each destination
            driver = load_driver()

            process_destination(driver, destination, check_in_date,
                                check_out_date)

    except Exception as e:
        error_msg = f"Exception occurred: {str(e)}"
        logger.error(error_msg)  # Use the custom logger
        # Handle the exception as per your requirement

    finally:
        end_time = time.time()  # End the timer
        execution_time = end_time - start_time
        logger.info(
            f"Execution time: {execution_time} seconds")  # Log execution time


if __name__ == '__main__':
    main()
