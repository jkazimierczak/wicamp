import json
import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import List


def load_json_from_file(filename: str):
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(1)


class TaskItemType(Enum):
    TASK_LESSON = auto()
    TASK_CONTENT = auto()
    QUESTION_FORM = auto()
    ANSWER_FORM = auto()


@dataclass
class CourseItem:
    name: str
    href: str


@dataclass
class CourseTask:
    index: int
    items: List["CourseTaskItem"]


@dataclass
class CourseTaskItem(CourseItem):
    type: TaskItemType


class Course:
    def __init__(self):
        self._content = None
        self.obligatory: List[CourseItem] = []
        self.lectures: List[CourseItem] = []
        self.tasks: List[CourseTask] = []

    def populate(self):
        self._content = load_json_from_file("course_links.json")
        self.obligatory = self.parse_content(self._content["obligatory"])
        self.lectures = self.parse_content(self._content["lectures"])
        self.tasks = self.parse_tasks(self._content["tasks"])
        return self

    def get_obligatory(self, query_str):
        """Search for a lecture. query_str can be a word, number or phrase."""
        for obligatory in self.obligatory:
            if str(query_str) in obligatory.name:
                return obligatory

    def get_lecture(self, query_str):
        """Search for a lecture. query_str can be a word, number or phrase."""
        for lecture in self.lectures:
            if str(query_str) in lecture.name:
                return lecture

    def get_task(self, task_num, item_type: TaskItemType = TaskItemType.TASK_LESSON):
        for task in self.tasks:
            if task.index == task_num:
                for item in task.items:
                    if item.type == item_type:
                        return item
                    # return item if item.type == item_type else

    def parse_content(self, section):
        items = []
        for item in section:
            parsed_item = CourseItem(item["name"], item["href"])
            items.append(parsed_item)
        return items

    def _type_from_string(self, s: str):
        """Translate string to matching CourseTaskItem"""
        for i in list(TaskItemType):
            if s.lower() == i.name.lower():
                return i

    def parse_tasks(self, section):
        items = []
        for i in section:
            task_items = []
            for item in section[i]:
                task_items.append(CourseTaskItem(
                    type=self._type_from_string(item["type"]),
                    name=item["name"],
                    href=item["href"]
                ))
            items.append(CourseTask(int(i), task_items))
        return items
