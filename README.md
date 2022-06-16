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
poetry install
```

## Running
Before running:
* install Firefox,
* edit rename `.evn.tempalte` to `.env` and update the info 
accordingly.

> GitHub token is necessary to download a correct WebDriver (gecko). To 
> create a personal token follow [this document](https://help.github.com/articles/creating-an-access-token-for-command-line-use).

After configuring the `.env` file run:
```bash
poetry run python main.py
```

And that's it! If you want you can customize visited pages in `main.py`.
