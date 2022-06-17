import time
from datetime import datetime, timedelta

import bs4
import selenium.common.exceptions
import selenium.webdriver
from rich.console import Console
from rich.text import Text
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from . import pages, course
from .strtime import strtime_diff
from .web_driver import WebDriver


class App:
    def __init__(self, username, password, driver: WebDriver):
        self.is_logged_in = False
        self.username = username
        self.password = password
        self._driver = driver
        self._login_time: datetime = None
        self.soup: bs4.BeautifulSoup = None
        self.soup_made_on: datetime = datetime.fromtimestamp(0)
        self.console = Console()

    def debug(self):
        """Empty function. Breakpointing gives access to self."""
        pass

    @property
    def is_soup_expired(self):
        return True if (datetime.now() - self.soup_made_on).seconds > 60 else False

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

    def soupify_activity_page(self):
        end_time = int(datetime.now().timestamp())
        start_time = int((datetime.now() - timedelta(days=30)).timestamp())
        self.driver.get(pages.WikampPages.sysop_time_spent + f"&from={start_time}&to={end_time}")

        self.soup = bs4.BeautifulSoup(self.driver.page_source, "lxml")
        self.soup_made_on = datetime.now()

    def get_total_activity_time(self):
        if self.is_soup_expired:
            self.soupify_activity_page()
        match = self.soup.select_one("#sample-elapsed")
        return match.text.replace("Całkowity czas", "").strip()

    def get_activity_time(self, query_text):
        """Get activity time for a matching string.
        query_text is trimmed to 80 chars."""
        if self.is_soup_expired:
            self.soupify_activity_page()
        report_tables = self.soup.select(".trainingreport td")
        match = next(filter(lambda x: query_text[:80] in x.text, report_tables), None)
        if not match:
            print(f'Queried string ("{query_text}") not found.')
            return

        return report_tables[(report_tables.index(match) + 1)].text.strip()

    def load_lesson_page(self, href):
        self.driver.get(href)
        try:
            yes_button = self.driver.find_element(By.CLASS_NAME, "btn-primary")
            yes_button.click() if "Tak" in yes_button.text else None
        except selenium.common.exceptions.NoSuchElementException:
            return

    def create_status(self, diff):
        _diff = (f"+{diff}min", "green") if diff != 0 else ""
        _total = (self.get_total_activity_time(), "bold")
        return Text.assemble("Udaję, że czytam... ", _diff, " (łączny czas w kursie: ", _total, ")")

    def wander(self, page: course.CourseItem, duration: timedelta = None):
        time_start = datetime.now()
        time_end = None
        if duration:
            time_end = time_start + duration
        initial_reported_time = self.get_activity_time(page.name)
        reported_time = None

        self.console.print(Text.assemble("Rozpoczynam czytanie ", (page.name, "gold1"), " na ",
                                         (f"{duration.seconds // 60} minut", "gold1")))
        self.console.print(Text.assemble(f"Obecny czas w tej aktyności: ", (initial_reported_time, "bold")))
        with self.console.status(f"Rozpoczęto czytanie {page.name}", spinner_style="white") as status:
            self.load_lesson_page(page.href)
            i = 0
            while (datetime.now() < time_end) if duration else True:
                if i % 5 == 0:
                    reported_time = self.get_activity_time(page.name)
                    status.update(self.create_status(strtime_diff(initial_reported_time, reported_time)))
                    self.load_lesson_page(page.href)
                self.driver.refresh()
                time.sleep(60)
                i += 1
            reported_time = self.get_activity_time(page.name)
            self.console.print(Text.assemble(
                "Skończono udawanie. Czas w tej aktywności: ",
                (f"{self.get_activity_time(page.name)}, ", "bold"),
                "łączny czas w kursie: ", (self.get_total_activity_time(), "bold"))
            )

    def close(self):
        """Shutdown and save temporary profile."""
        self._driver.close()
