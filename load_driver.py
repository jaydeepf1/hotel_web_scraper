import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from find_free_port import find_free_port  # Make sure find_free_port is correctly implemented

def load_options():
    options = Options()
    options.use_chromium = True  # Ensure you are using Chromium-based Edge
    options.add_argument("--log-level=3")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("window-size=3000x3000")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # options.add_argument("--headless=new")
    return options

def load_driver():
    options = load_options()
    try:
        chrome_driver_port = find_free_port()  # Ensure find_free_port() is correctly implemented
        print(f"Using port: {chrome_driver_port}")
    except RuntimeError as e:
        print(f"Error finding a free port: {e}")
        exit(1)
    service = Service(port=chrome_driver_port)
    driver = webdriver.Chrome(service=service, options=options)
    return driver
