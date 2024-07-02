import configparser
import ast
from datetime import datetime, timedelta


class Config:
    def __init__(self, filename="config.ini"):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(self.filename)

    def save(self):
        with open(self.filename, "w") as configfile:
            self.config.write(configfile)

    def get(self, section, key):
        return self.config.get(section, key)

    def get_list(self, section, key):
        return ast.literal_eval(self.config.get(section, key))

    def get_int(self, section, key):
        return int(self.config.get(section, key))

    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))


class ConfigBuilder:
    def __init__(self, number_of_days=3):
        self.number_of_days = number_of_days

    def create_date_pairs(self):
        num_dates = self.number_of_days + 1
        start_date = datetime.now()
        dates = [start_date + timedelta(days=i) for i in range(num_dates)]
        date_pairs = list(zip(dates[:-1], dates[1:]))
        return tuple(
            (date1.strftime("%m/%d/%Y"), date2.strftime("%m/%d/%Y"))
            for date1, date2 in date_pairs
        )

    def build_config(self):
        config = Config()

        # Set default configurations
        config.set("WEBSITE", "URL", "https://www.ihg.com/hotels/us/en/reservation")
        config.set(
            "FORM",
            "Destinations",
            [
                "Chattanooga Lovell Airport, TN, United States",
                "Chattanooga, TN, United States",
                "Louisville, KY, United States",
                "College Station, TX, United States",
                "Baton Rouge, LA, USA",
                "Auburn, Alabama, United States",
            ],
        )
        config.set("FORM", "Dates", self.create_date_pairs())
        config.set("TIMER", "WebDriverWaitTimeOut", "120")
        config.set("TIMER", "CookieWait", "5")
        config.set("CHROMESERVICE", "Ports", tuple(range(1000, 10000, 100)))
        config.set("LOGGER", "BrowserLogPath", "logs/browser.log")

        config.save()


class ConfigReader:
    def __init__(self, filename="config.ini"):
        self.config = Config(filename)

    def get_destination_and_dates(self, destination):
        destinations = self.config.get_list("FORM", "Destinations")
        if destination in destinations:
            dates = self.config.get_list("FORM", "Dates")
            return destination, dates

    def get_logger_path(self, log_type):
        if log_type == "browser_log_path":
            return self.config.get("LOGGER", "BrowserLogPath")

    def get_time(self, time_type):
        if time_type == "COOKIE_WAIT":
            return self.config.get_int("TIMER", "CookieWait")
        elif time_type == "DRIVER_WAIT":
            return self.config.get_int("TIMER", "WebDriverWaitTimeOut")

    def get_URL(self):
        return self.config.get("WEBSITE", "URL")


if __name__ == "__main__":
    # Build or update the configuration file
    builder = ConfigBuilder()
    builder.build_config()

    # Example usage of the ConfigReader class
    reader = ConfigReader()
    print(
        "Destination and Dates:",
        reader.get_destination_and_dates("Chattanooga, TN, United States"),
    )
    print("Browser Log Path:", reader.get_logger_path("browser_log_path"))
    print("Cookie Wait Time:", reader.get_time("COOKIE_WAIT"))
    print("Web Driver Wait Timeout:", reader.get_time("DRIVER_WAIT"))
    print("Website URL:", reader.get_URL())
