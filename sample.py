from src.testproject.sdk.drivers import webdriver

REPOS = ['find-kedro', 'kedro-static-viz', 'kedro-action', 'steel-toes', ]
RSS = 'https://waylonwalker.com/rss'

# def test_all_links(driver, url):
    

def test_title_on_every_page(driver):
    feed = feedparser.parse("https://waylonwalker.com/rss")['entries']
    for post in feed:
        driver.get(post['link'])

# @report(test='Test Repos Loaded')
def test_repos_loaded():
    """
    Test that GitHub repo cards are loaded client side.
    """
    driver = webdriver.Chrome()
    repo_elements = driver.find_elements_by_class_name('repo')
    header_text = [header.text for header in driver.find_elements_by_class_name("repo-name")]
    for repo in REPOS:
        if repo not in header_text:
            return False
        print(f'{repo} has an h2 tag') 
    driver.quit()
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
    print('testing GitHub repos')
    test_repos_loaded()
    # print('testing title on page')
    # test_title_on_every_page(driver)

    driver.quit()
