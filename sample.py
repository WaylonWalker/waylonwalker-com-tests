from src.testproject.sdk.drivers import webdriver

if __name__ == "__main__":
    driver = webdriver.Chrome()

    driver.get("https://waylonwalker.com/")

    passed = driver.find_element_by_css_selector("section.about").is_displayed()

    print("Test passed") if passed else print("Test failed")

    driver.quit()
