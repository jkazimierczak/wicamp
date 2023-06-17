<h1 align="center">WICAMP</h1>
<p align="center"><i>"Because sitting at the CAMPfire and staring at it is more 
  enjoyable than staring 30 hours at WICAMP pages."</i></p>

This goal of this scripts is to effortlessly reach a minimum of 30 hours on a 
course 
pages
and go beyond that.

Features:
* works headless (no visible browser window), 
* can run in the background,
* it prints the progress made on the console,
* it rotates the pages,
* randomizes the time spent on a single page.

## Installation
To install just clone this repository and install dependencies. This 
requires you to have poetry installed.
```bash
git clone https://github.com/jkazimierczak/wicamp.git
cd wicamp
poetry install
```

## Running
Before running:
* install Firefox,
* rename `.evn.tempalte` to `.env` and update the info accordingly.
> If you're using it in different course edition, you will need to edit `course_links.json`.

> GitHub token is necessary to download a correct WebDriver (gecko). To 
> create a personal token follow [this document](https://help.github.com/articles/creating-an-access-token-for-command-line-use). 
> The token doesn't have to have any permissions. Both fine-grained and classic
> tokens will work.

After editing the `.env` you can begin to use the program.
```bash
# Generate a link to statistics from last 30 days
poetry run python -m wicamp mystats

# Run for specific lectures
poetry run python -m wicamp run --lectures 11,12,13,14,15
```
> Type `poetry run python -m wicamp run --help` to see all available activities.
