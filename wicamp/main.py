import datetime
import itertools
import os
import random
import sys
from typing import List, Union

from dotenv import load_dotenv

from wicamp.app import App, ActivityTimeNotFound
from wicamp.course import Course, TaskItemType
from wicamp.web_driver import WebDriver

load_dotenv()

if os.environ["WDM_LOG"] == "false":
    import logging

    logging.getLogger('WDM').setLevel(logging.NOTSET)


def main(
        lectures: List[Union[str, int]],
        lessons,
        tasks,
        question_forms,
        answer_forms
):
    username = os.environ["WICAMP_USERNAME"]
    password = os.environ["WICAMP_PASSWORD"]

    course = Course().populate()
    driver = WebDriver()
    app = App(username, password, driver)

    items = []
    for lecture in lectures:
        items.append(course.get_lecture(lecture))
    for lesson in lessons:
        items.append(course.get_task(lesson, TaskItemType.TASK_LESSON))
    for task in tasks:
        items.append(course.get_task(task, TaskItemType.TASK_CONTENT))
    for question_form in question_forms:
        items.append(course.get_task(question_form, TaskItemType.QUESTION_FORM))
    for answer_form in answer_forms:
        items.append(course.get_task(answer_form, TaskItemType.ANSWER_FORM))
    items = [item for item in items if item is not None]

    app.ftims_login()
    items = app.create_activity_lookup_table(items)
    # random.shuffle(items)
    for item in itertools.cycle(items):
        minutes = random.randint(15, 60)
        try:
            app.wander(item, datetime.timedelta(minutes=minutes))
        except ActivityTimeNotFound as err:
            link = "[link=https://github.com/jkazimierczak/wicamp/issues/5]issue #5[/link]"
            app.console.print("[red]Error: Couldn' get activity time for this course.[/red]\n"
                              f"Please reopen {link} and paste this string with quotes:\n```{err}```",
                              highlight=False)
            items.remove(item)
        except KeyboardInterrupt:
            print("Exiting")
            app.close()
            sys.exit(0)
    app.close()


if __name__ == "__main__":
    main()
