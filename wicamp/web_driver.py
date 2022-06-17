from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


class WebDriver:
    def __init__(self):
        self.driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            options=self.create_options(),
        )

    def create_options(self):
        options = Options()
        options.headless = True
        return options

    def close(self):
        self.driver.close()
