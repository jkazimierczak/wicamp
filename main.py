import os

from dotenv import load_dotenv

from wicamp.app import App
from wicamp.course import Course
from wicamp.web_driver import WebDriver

load_dotenv()


def main():
    username = os.environ["WICAMP_USERNAME"]
    password = os.environ["WICAMP_PASSWORD"]

    course = Course().populate()
    driver = WebDriver()
    app = App(username, password, driver)
    app.debug()
    app.ftims_login()
    # 2h 39min
    app.wander(course.get_task(4))
    # TODO: Implement time check to validate the progress
    app.close()


if __name__ == "__main__":
    main()
