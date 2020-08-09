# Testing Client-Side Scripts with Pytest in GitHub Actions
_by [waylon walker](https://waylonwalker.com)_

This article will cover client-side testing interactions with TestProject, pytest, and run it inside of GitHub actions.  If your GitHub repo is public, this will be 100% free.  This is great for learning TestProject, running integration testing on your side projects.  If you need the security of running your actions from a private repo, GitHub offers a very generous amount of free minutes https://github.com/features/actions#pricing-details.

## GitHub Repo Cards

I chose to start with the GitHub repos as they seemed a bit more straightforward, and it's been a while since I have done any selenium.

[waylonwalker.com](https://waylonwalker.com/) has his favorite repositories pinned to the top of the website.  The information for these cards is dynamic and pulled in from the GitHub API client side.  This means that as the pages load, JavaScript will execute scripts to pull information from the GitHub API, then transform that data into the DOM, and render it on the page.

<p align='center' style='text-align: center'>
<img src='https://waylonwalker.com/open-source-cards.png' width='500' style='width:500px; max-width:80%; margin: auto;' alt='Open Source cards as they look on waylonwalker.com'/>
</p>

> here is what the GitHub repo cards look like

## Get Your Keys

The first thing that you are going to need is a [TP\_DEV\_TOKEN ](https://app.TestProject.io/#/integrations/sdk) and [TP\_API\_KEY](https://app.TestProject.io/#/integrations/api).  These will give TestProject access to your account to automatically post results to your [dashboard](https://app.TestProject.io/#/reports).

* [TP\_DEV\_TOKEN ](https://app.TestProject.io/#/integrations/sdk)
* [TP\_API\_KEY](https://app.TestProject.io/#/integrations/api)

### Put these in secrets in your repo

In your GitHub repo, go to `settings>Secrets`, or append `settings/secrets` to the URL to your repo, and add the tokens.  This will give GitHub safe access to them without them being available to the public, contributors, log files, or anything.


<p style='text-align: center'>
<img src='https://waylonwalker.com/test-waylonwalker-com-secrets.png' style='width:600px; max-width:80%; margin: auto;' alt='Secrets panel in the GitHub Repo'/>
</p>

---

## Setup Dev
_optional_

To expedite development, I went ahead and set up a development environment in Digital Ocean.  This step is optional, and everything can run from your local machine, or entirely from GitHub actions.  I felt like setting up an Ubuntu Droplet in Digital Ocean gave me a very close to production feel that I could quickly iterate. This allowed me to get all of my tests working a bit quicker than just running them through GitHub, but being as similar as possible.  This allowed me to learn the ins and outs of setting up TestProject without needing to do a full install every time GitHub actions ran.

<p align='center' style='text-align: center'>
<a href='https://waylonwalker.com/notes/new-machine-tpio'>
  <img
    width='500'
    style='width:500px; max-width:80%; margin: auto;'
    src="https://waylonwalker.com/new-machine-tpio-rm.png"
    alt="Test Project Dev Machine setup notes card"
  />
  </a>
</p>
> I am not going to go into full dev machine setup here, but you can read my [setup notes](https://waylonwalker.com/notes/new-machine-tpio).

---

## 🐍 Pytest
_you can see all of the tests ran with pytest on [github](https://github.com/waylonwalker/waylonwalker-com-tests/tree/master/tests)_

I chose to go down the route of using pytest.  I liked the idea of utilizing fixtures, automatically running my test functions, and using a bit of the pytest reporting capabilities as I was developing.  TestProject does not need to run through a test framework like pytest, 

**NOTE** per pytest standard practice, I named the directory containing tests `tests`.  While this works, TestProject.io uses this directory as the default name for the project.  If I were to go back, I would either rename the directory to what I wanted to show up on TestProject.io or configure the project name inside the config.


## conftest.py
_You can see the [conftest.py](https://github.com/WaylonWalker/waylonwalker-com-tests/blob/master/tests/conftest.py) live on GitHub._


[conftest.py](https://github.com/WaylonWalker/waylonwalker-com-tests/blob/master/tests/conftest.py) is a common to place fixtures that are used by multiple modules. Pytest automatically imports all [conftest.py](https://github.com/WaylonWalker/waylonwalker-com-tests/blob/master/tests/conftest.py) modules from the same directory that you are working from. This is a great place to include TesProject driver fixtures.  Note that when you use a fixture as an argument in another function, the fixture will do setup, pass anything from the yield statement to the test function, run the test function, then run teardown.

> conftest.py stores fixtures for all modules in a directory.

``` python
# tests/conftest.py

import time
import pytest
from src.TestProject.sdk.drivers import web driver

@pytest.fixture
def driver():
    "creates a webdriver and loads the homepage"
    driver = webdriver.Chrome()
    driver.get("https://waylonwalker.com/")
    yield driver
    driver.quit()
```

> The full version of [conftest.py](https://github.com/WaylonWalker/waylonwalker-com-tests/blob/master/tests/conftest.py) is available on GitHub

The above sample is a bit **simplified**.  I ran into some inconsistencies in the real version and found that some tests had a better pass rate if I added a `time.sleep` statement.  In my full project, I ended up with a `driver` and a `slow_driver` fixture. This allowed me to have a driver that waited for JavaScript to execute just a bit longer.

## test_repos.py

_The full version of [testrepos.py](waylonwalker.com/testrepos.py) is available on GitHub_


I have initially set up three different tests for the repo cards.  I set a list of repos that I expect to show up in the cards.  These tests are quite easy to do with TestProject.io as it uses selenium and a headless browser to execute javascript under the hood.  The `REPOS` area created as a global list here and can easily be refactored into a config file if the time ever comes that they need to be.

If you are not familiar, a **headless browser** runs the engine as your browser without a graphical user interface.  JavaScript gets fully loaded and parsed, and the dom is completely interactive programmatically.

Read through the docstrings of each function as it describes what happens at each step.

``` python
"""
Test that GitHub repo data dynamically loads the client-side.
"""

REPOS = [
    "find-kedro",
    "kedro-static-viz",
    "kedro-action",
    "steel-toes",
]

def test_repos_loaded(slow_driver):
    """
    Test that each repo-name exists as a title in one of the repo cards.

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
    Ensure that stars are correctly parsed from the API and loaded client-side

    On waylonwalker.com repo cards have a stars element with a class of "repo-stars" and
    is displayed as "n stars"
    """
    repo_elements = slow_driver.find_elements_by_class_name("repo")
    for el in repo_elements:
        stars = el.find_element_by_class_name("repo-stars")
        num_stars, label = stars.text.split()
        assert int(num_stars) > 0
        assert label == 'stars'
```

## Forum
_[forum.TestProject.io](https://forum.TestProject.io/t/install-agent-inside-github-actions/2334/3)_

I was a bit confused about how to set up TestProject.io inside of actions. The forum welcomed me with a prompt response linking to the exact example I needed.  The example was written in java but had set up the docker-compose steps that I needed.

---

## GitHub Actions 🎬

_[test-waylonwalker-com.yml](https://github.com/WaylonWalker/waylonwalker-com-tests/blob/master/.github/workflows/test-waylonwalker-com.yml_

Now that I have my GitHub repo setup with my [tests](https://github.com/WaylonWalker/waylonwalker-com-tests/tree/master/tests) successfully running in pytest let's get it running inside of GitHub actions automatically.

Actions are GitHub's solution to CI/CD.  It allows you to execute code within a virtual machine managed by GitHub that can get extra information from your repo, such as secrets, which we set up at the beginning.  What gets ran, how it gets ran, and when it gets ran are all configured inside of a `yaml` file.


``` yaml
# .github/workflows/test-waylonwalker-com.yml
name: Test WaylonWalker.com

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '*/10 * * * *'
```

You can see in the section above I have set up to run every time there is a push to or pull request open to main.  I also set a reasonably aggressive test schedule to run every **10** **minutes**.  This is just to build confidence in the tests and get more data in the reports to explore.  I will likely turn this down later.

``` yaml

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@main
    - uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - run: pip install -r requirements.txt
    - name: Run TestProject Agent
      env:
        TP_API_KEY: ${{ secrets.TP_API_KEY }} # < Let Secrets handle your keys
      run: |
        envsubst < .github/ci/docker-compose.yml > docker-compose.yml
        cat docker-compose.yml
        docker-compose -f docker-compose.yml up -d
    - name: Wait for Agent to Register
      run: bash .github/ci/wait_for_agent.sh
    - run: pytest
      env:
        TP_DEV_TOKEN: ${{ secrets.TP_DEV_TOKEN }} # < Let Secrets handle your tokens
        TP_AGENT_URL: http://localhost:8585
```

In the test job, you can see that I have decided to run the test job on `ubuntu-latest`.  The first three steps are a bit of boilerplate to checkout the repo, setup python 3.8, and pip install our `requirements.txt`.  Next, the [TP\_API\_KEY](https://app.TestProject.io/#/integrations/api) has been rendered into the [docker-compose.yml](https://github.com/WaylonWalker/waylonwalker-com-tests/blob/master/.github/ci/docker-compose.yml) using `envsubst`, `docker-compose` has been started, and waited for the agent to be ready.  I have also exposed our [TP\_DEV\_TOKEN ](https://app.TestProject.io/#/integrations/sdk) to pytest and ran pytest.


## docker-compose.yml

_[docker-compose.yml](https://github.com/WaylonWalker/waylonwalker-com-tests/blob/master/.github/ci/docker-compose.yml)_

The following [docker-compose.yml](https://github.com/WaylonWalker/waylonwalker-com-tests/blob/master/.github/ci/docker-compose.yml) file was graciously contributed by [@vitalybu](https://github.com/vitalybu) in the [testproject-io/java-sdk](https://github.com/testproject-io/java-sdk/blob/master/.github/ci/docker-compose.yml) repo.  It sets up a template with the **`TP_API_KEY`** as a variable for envsubst, headless browsers for chrome and firefox, and the TestProject.io agent.

``` yaml
version: "3.1"
services:
  testproject-agent:
    image: testproject/agent:latest
    container_name: testproject-agent
    depends_on:
      - chrome
      - firefox
    environment:
      TP_API_KEY: "${TP_API_KEY}"
      TP_AGENT_TEMP: "true"
      TP_SDK_PORT: "8686"
      CHROME: "chrome:4444"
      CHROME_EXT: "localhost:5555"
      FIREFOX: "firefox:4444"
      FIREFOX_EXT: "localhost:6666"
    ports:
    - "8585:8585"
    - "8686:8686"
  chrome:
    image: selenium/standalone-chrome
    volumes:
      - /dev/shm:/dev/shm
    ports:
    - "5555:4444"
  firefox:
    image: selenium/standalone-firefox
    volumes:
      - /dev/shm:/dev/shm
    ports:
    - "6666:4444"
```

## ⌚ Waiting for the agent to register
_[wait for agent.sh](https://waylonwalker.com/waitforagent.sh)_

I think the most interesting part of the workflow above is how we wait for the agent to register.  The shell script is a bit terse.  It looks for exceeding the `max_attempts` allowed or that the agent has started by using its `/api/status` rest API.  This prevents us from wasting too much time by setting a big wait or trying to move on too early and running pytest without a running agent.

``` bash
trap 'kill $(jobs -p)' EXIT
attempt_counter=0
max_attempts=100
mkdir -p build/reports/agent
docker-compose -f docker-compose.yml logs -f | tee build/reports/agent/log.txt&
until curl -s http://localhost:8585/api/status | jq '.registered' | grep true; do
    if [ ${attempt_counter} -eq ${max_attempts} ]; then
    echo "Agent failed to register. Terminating..."
    exit 1
    fi
    attempt_counter=$(($attempt_counter+1))
    echo
    sleep 1
done
```


## TestProject.io Dashboard 〽

Once the tests are running, they will appear in the TestProject dashboard.  There are several failures that happened early on in the development of the tests, but they continued to pass once they started passing.


<p align='center' style='text-align: center'>
  <img
    width='800'
    style='width:800px; max-width:80%; margin: auto;'
    src="https://waylonwalker.com/tpio-test-repos.png"
    alt="My Dashboard for test_repos"
  />
</p>

## A single test flow in the dashboard

The dashboard lets you drill in to see individual tests that have been run, select them, and examine individual reports for each test. It converts the steps ran by the driver into a human-readable _flowchart_, and each step can be opened up to see the values that were pulled from the site by the driver.


<p align='center' style='text-align: center'>
  <img
    width='350'
    style='width:350px; max-width:80%; margin: auto;'
    src="https://waylonwalker.com/test_repo_stars_loaded.png"
    alt="driver flow of test_repo_stars_loaded"
  />
</p>

## Authored by Waylon Walker

This page was created by [waylon walker](https://waylonwalker.com) based on his article ([Integration testing with Python, TestProject.io, and GitHub Actions](https://waylonwalker.com/blog/testproject-io-py-actions/)).

