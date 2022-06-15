import time
from datetime import datetime

import requests
import selenium.common.exceptions
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from . import pages
from .course import Course
from .web_driver import WebDriver


class App:
    def __init__(self, username, password, driver: WebDriver):
        self.is_logged_in = False
        self.username = username
        self.password = password
        self._driver = driver
        self._login_time: datetime = None
        self.session = requests.Session()

    def debug(self):
        """Empty function. Breakpointing gives access to self."""
        pass

    @property
    def login_time(self) -> int:
        if not self._login_time:
            return 0
        return (datetime.now() - self._login_time).seconds

    @property
    def driver(self):
        return self._driver.driver

    def check_if_logged_in(self):
        self.driver.get(pages.WikampPages.cas)
        WebDriverWait(self.driver, 3).until(EC.any_of(
            EC.presence_of_element_located((By.NAME, "submit")),
            EC.presence_of_element_located((By.CLASS_NAME, "fullname"))
        ))

        if "cas." in self.driver.current_url:
            self.is_logged_in = False
        if "virtul." in self.driver.current_url:
            self.is_logged_in = True
        return self.is_logged_in

    def cas_login(self):
        if self.check_if_logged_in():
            return
        else:
            if self.driver.current_url != pages.WikampPages.cas_login:
                self.driver.get(pages.WikampPages.cas_login)
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.NAME, "submit"))
            )

        try:
            login_box = self.driver.find_element(by=By.NAME, value='username')
            password_box = self.driver.find_element(by=By.NAME, value='password')
        except selenium.common.exceptions.NoSuchElementException as err:
            print("LOGIN_PAGE:", err)
            return

        login_box.send_keys(self.username)
        password_box.send_keys(self.password)
        password_box.submit()
        time.sleep(5)

        self.is_logged_in = True
        self._login_time = datetime.now()

    def ftims_login(self):
        if not self.is_logged_in:
            self.cas_login()

        self.driver.get(pages.WikampPages.ftims_login)
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.ID, "login"))
        )

        student_login_box = self.driver.find_element(by=By.ID, value='login')
        student_login_box.click()
        time.sleep(5)

    def go_to_course(self, course: Course):
        self.driver.get(course.value)
        # time.sleep(5)

    def wander(self, page: pages.SysopLectures):
        self.driver.get(page.value)
        while True:
            print(f"Refreshing {page.name}")
            self.driver.refresh()
            time.sleep(60)
            # TODO: Implement refreshing timeout

    def close(self):
        """Shutdown and save temporary profile."""
        self._driver.close()
