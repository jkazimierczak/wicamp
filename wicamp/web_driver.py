import pickle
from typing import List

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


class WebDriver:
    def __init__(self):
        self.driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            options=self.create_options(),
        )
        self.cookies: List[dict] = self._load_cookies()

    def create_options(self):
        options = Options()
        options.headless = True
        return options

    def _load_cookies(self):
        try:
            with open("../cookiejar", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return

    def get_domain_cookies(self, domain: str):
        results = []
        for cookie in self.cookies:
            if domain in cookie.get("domain"):
                results.append(cookie)
        return results

    def close(self):
        with open("../cookiejar", "wb") as f:
            pickle.dump(self.driver.get_cookies(), f)
        self.driver.close()
