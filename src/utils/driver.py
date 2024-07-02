import time
from selenium.webdriver import Chrome, ChromeOptions


class Driver:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def _get_options():
        options = ChromeOptions()

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extentsions")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--headless=new")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
        )

        return options

    def get_driver(self):
        options = Driver._get_options()
        chrome_driver = Chrome(options=options)
        chrome_driver.get(self.url)
        chrome_driver.maximize_window()
        time.sleep(3)
        return chrome_driver
