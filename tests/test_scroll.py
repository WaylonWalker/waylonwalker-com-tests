"Test that more cards load after scrolling"
from src.testproject.sdk.drivers import webdriver
import time

def test_cards_load(driver):
    "test that cards load on the page, and more load as we scroll"
    num_cards = []
    num_cards.append(len(driver.find_elements_by_class_name('post-wrapper')))

    driver = webdriver.Chrome()
    driver.execute_script("window.scrollTo(0, 100000)")
    # time.sleep(3)
    num_cards.append(len(driver.find_elements_by_class_name('post-wrapper')))

    # test that cards are loaded
    assert num_cards[0] >= 3
    # test that more cards are loaded after scrolling
    assert num_cards[0] > num_cards[1]

