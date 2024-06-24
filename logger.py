import logging

def set_log():
    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the base level to the lowest to capture all levels

    # Check if logger already has handlers to avoid duplicate handlers
    if not logger.hasHandlers():
        # Create handlers
        error_file_handler = logging.FileHandler('error.log')
        error_file_handler.setLevel(logging.ERROR)  # Log only ERROR level messages to the file

        info_file_handler = logging.FileHandler('info.log')
        info_file_handler.setLevel(logging.INFO)  # Log INFO and WARNING level messages to the file

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Log INFO and above level messages to the console

        # Create formatters and add them to the handlers
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        error_file_handler.setFormatter(file_formatter)
        info_file_handler.setFormatter(file_formatter)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # Add handlers to the logger
        logger.addHandler(error_file_handler)
        logger.addHandler(info_file_handler)
        logger.addHandler(console_handler)

    return logger
