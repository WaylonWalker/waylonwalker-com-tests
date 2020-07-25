from src.testproject.sdk.drivers import webdriver

if __name__ == "__main__":
    driver = webdriver.Chrome()

    driver.get("https://waylonwalker.com/")
    headers = driver.find_elements_by_tag_name("h2")
    
    passed = headers[0].is_displayed()
    
    print('number of headers: ', len(headers))
    print("Test passed") if passed else print("Test failed")

    driver.quit()
