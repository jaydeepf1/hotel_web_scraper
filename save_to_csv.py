import csv
import os
from logger import set_log

# Initialize the custom logger
logger = set_log()

def save_to_csv(data, filename='hotel_data.csv'):
    """
    Save data to a CSV file in the 'data' folder.

    Args:
    - data (list of dicts): Data to be saved in CSV format.
    - filename (str): Name of the CSV file. Default is 'hotel_data.csv'.
    """
    if data:
        keys = data[0].keys()

        # Ensure the 'data' folder exists, create if it doesn't
        folder_path = 'data'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Construct the full file path
        file_path = os.path.join(folder_path, filename)

        try:
            # Write data to CSV file
            with open(file_path, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)

            logger.info(f"Data saved to {file_path}")  # Use the custom logger
        except Exception as e:
            error_msg = f"Error occurred while saving data to {file_path}: {str(e)}"
            logger.error(error_msg)  # Use the custom logger
            # Handle the exception as per your requirement
    else:
        logger.warning("No data to save")  # Use the custom logger
