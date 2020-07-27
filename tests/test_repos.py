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
    Test that GitHub repo cards are loaded client side.
    """
    repos = slow_driver.find_elements_by_class_name("repo-name")
    header_text = [
        header.text for header in repos
    ]
    for repo in REPOS:
        assert repo in header_text


def test_repo_description_loaded(slow_driver):
    "Test that each repo has a description longer than 10 characters"
    repo_elements = slow_driver.find_elements_by_class_name("repo")
    for el in repo_elements:
        desc = el.find_element_by_class_name("repo-description")
        assert len(desc.text) > 10


def test_repo_stars_loaded(slow_driver):
    repo_elements = slow_driver.find_elements_by_class_name("repo")
    for el in repo_elements:
        stars = el.find_element_by_class_name("repo-stars")
        num_stars, label = stars.text.split()
        assert int(num_stars) > 0
        assert label == 'stars'
