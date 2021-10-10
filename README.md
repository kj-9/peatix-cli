# peatix_cli

Command line tool to search and featch [peatix](https://peatix.com/) events and output a table to screen.

## Install

### Prerequisite
1. You need Google Chrome installed.
2. You need [chromedriver](https://sites.google.com/chromium.org/driver/downloads) executable installed. (You can also specify the path to chromedriver executable by the `--chromedriver` argument from cli.)

### Build from source
Crone this repo, and run:

```bash
pip install --upgrade setuptools build
python -m build
pip install .\dist\peatix_cli-0.0.1-py3-none-any.whl
```

## Usage
```
$ peatix search -h

usage: peatix search [-h] [--chromedriver CHROMEDRIVER] [--max_page MAX_PAGE] [--period {today,this_weekend,next_week,}] [--show_link] [--tag_id TAG_ID]

optional arguments:
  -h, --help            show this help message and exit
  --chromedriver CHROMEDRIVER
                        path to chromedriver executable
  --max_page MAX_PAGE   miximum number of pages to featch results, (default: 30)
  --period {today,this_weekend,next_week,}
                        filter if date of events is in period, set '' to not to filter, (default: this_weekend)
  --show_link           if this flag is set, show a bare url link instead of an embedded link
  --tag_id TAG_ID       filter by tag_id
```


## Development

```bash
pip install -r requirements.txt
pip install -e .
```
