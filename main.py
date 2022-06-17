import datetime
import os
import random

from dotenv import load_dotenv

from wicamp.app import App
from wicamp.course import Course, TaskItemType
from wicamp.web_driver import WebDriver

load_dotenv()

if os.environ["WDM_LOG"] == "false":
    import logging

    logging.getLogger('WDM').setLevel(logging.NOTSET)


def main():
    username = os.environ["WICAMP_USERNAME"]
    password = os.environ["WICAMP_PASSWORD"]

    course = Course().populate()
    driver = WebDriver()
    app = App(username, password, driver)
    app.ftims_login()
    items = [
        course.get_obligatory("Regulamin labo"),
        course.get_obligatory("Regulamin przed"),
        course.get_obligatory("Harmonogram"),
        course.get_task(4),
        course.get_task(4, TaskItemType.ANSWER),
        course.get_task(4, TaskItemType.QUESTION),
        course.get_lecture(14),
        course.get_lecture(15)
    ]
    random.shuffle(items)
    i = 0
    while i <= len(items):
        if i == len(items):
            print("Mieszam w kotle, ustalam nowa kolejnosc")
            i = 0
            random.shuffle(items)
            continue

        item = items[i]
        minutes = random.randint(15, 60)
        app.wander(item, datetime.timedelta(minutes=minutes))
        i += 1
    app.close()


if __name__ == "__main__":
    main()
