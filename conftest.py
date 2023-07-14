import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from distutils.util import strtobool

from common_strings import URLs


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Specify chrome, firefox or safari"
    )

    parser.addoption(
        "--env", action="store", default="dev", help="Specify dev or prod"
    )

    parser.addoption(
        "--headless", action="store", default=True, help="Specify True or False", type=lambda x: bool(strtobool(x))
    )


@pytest.fixture(scope="function")
def browser(request):
    browser_option = request.config.getoption("--browser")
    headless_mode = request.config.getoption("--headless")

    # Set browser based on option
    if browser_option.lower() == "chrome":
        options = ChromeOptions()
        if headless_mode:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    elif browser_option.lower() == "firefox":
        options = FirefoxOptions()
        if headless_mode:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif browser_option.lower() == "safari":
        options = SafariOptions()
        if headless_mode:
            options.add_argument("--headless")
        driver = webdriver.Safari(options=options)
    else:
        raise ValueError("Invalid browser specified")

    request.cls.driver = driver

    # TODO: Go to URL based on environment
    driver.get(URLs.SAUCE_DEMO)

    def teardown():
        driver.quit()

    request.addfinalizer(teardown)
