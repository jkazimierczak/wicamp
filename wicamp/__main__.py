from datetime import datetime, timedelta

import typer

from wicamp import pages
from wicamp.main import main

cli = typer.Typer()


def split_str_arg(arg: str):
    return arg.split(",")


@cli.command()
def run(
        lectures: str = typer.Option("", help="Indexes of lectures"),
        lessons: str = typer.Option("", help="Indexes of lessons"),
        tasks: str = typer.Option("", help="Number(s) of task(s)"),
        question_forms: str = typer.Option("", help="Number(s) of task(s) that have the question form"),
        answer_forms: str = typer.Option("", help="Number(s) of task(s) that have the answer form"),
):
    """
    Start "reading" specified item. Numbers correspond to the task/lecture.
    """
    lectures = split_str_arg(lectures)
    lessons = split_str_arg(lessons)
    tasks = split_str_arg(tasks)
    question_forms = split_str_arg(question_forms)
    answer_forms = split_str_arg(answer_forms)

    main(lectures, lessons, tasks, question_forms, answer_forms)


@cli.command()
def mystats():
    """
    Generate a link for page with stats from last 30 days.
    """
    end_time = int(datetime.now().timestamp())
    start_time = int((datetime.now() - timedelta(days=30)).timestamp())
    typer.echo(pages.WikampPages.sysop_time_spent + f"&from={start_time}&to={end_time}")


if __name__ == "__main__":
    cli()
