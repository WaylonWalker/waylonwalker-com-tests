import time
import pytest
from src.testproject.sdk.drivers import webdriver

def get_driver(wait_time=0):
    "creates a webdriver and loads the homepage"
    driver = webdriver.Chrome()
    driver.get("https://waylonwalker.com/")
    time.sleep(wait_time) # wait for the GitHub api to load on the page
    return driver

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture
def slow_driver():
    driver = get_driver(10)
    yield driver
    driver.quit()

