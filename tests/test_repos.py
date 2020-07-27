"""
Test that GitHub repo data dynamically loads client side.
"""

REPOS = [
    "find-kedro",
    "kedro-static-viz",
    "kedro-action",
    "steel-toes",
]

def test_repos_loaded(slow_driver):
    """
    Test that the each repo-name exists as a title in one of the repo cards.

    On waylonwalker.com repo cards have a title with a class of "repo-name"
    """
    repos = slow_driver.find_elements_by_class_name("repo-name")
    # get innertext from elements
    header_text = [
        header.text for header in repos
    ]
    for repo in REPOS:
        assert repo in header_text


def test_repo_description_loaded(slow_driver):
    """
    Test that each repo has a description longer than 10 characters
    
    On waylonwalker.com repo cards have a descriptiion with a class of "repo-description"
    """
    repo_elements = slow_driver.find_elements_by_class_name("repo")
    for el in repo_elements:
        desc = el.find_element_by_class_name("repo-description")
        assert len(desc.text) > 10


def test_repo_stars_loaded(slow_driver):
    """
    Ensure that stars are properly parsed from the api and loaded client side

    On waylonwalker.com repo cards have a stars element with a class of "repo-stars" and
    is displayed as "n stars"
    """
    repo_elements = slow_driver.find_elements_by_class_name("repo")
    for el in repo_elements:
        stars = el.find_element_by_class_name("repo-stars")
        num_stars, label = stars.text.split()
        assert int(num_stars) > 0
        assert label == 'stars'
