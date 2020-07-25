from src.testproject.sdk.drivers import webdriver

REPOS = ['find-kedro', 'kedro-static-viz', 'kedro-action', 'steel-toes', ]

def test_github_packages(driver):
    "check that each repo is represented in an h2"
    header_text = [header.text for header in driver.find_elements_by_tag_name("h2")]
    for repo in REPOS:
        if repo not in header_text:
            return False
        print(f'{repo} has an h2 tag')
    return True
        
    

if __name__ == "__main__":
    driver = webdriver.Chrome()

    driver.get("https://waylonwalker.com/")
    headers = driver.find_elements_by_tag_name("h2")
    
    passed = headers[0].is_displayed()
    
    print('these are the headers')
    print([header.text for header in driver.find_elements_by_tag_name("h2")])
    print()
    print('number of headers: ', len(headers))
    print("Test passed") if passed else print("Test failed")

    driver.quit()
