# peatix_cli

Command line tool to search and featch [peatix](https://peatix.com/) events and output a table to screen.

# Install


1. You need Google Chrome installed.
2. You need [chromedriver](https://sites.google.com/chromium.org/driver/downloads) executable installed. (You can also specify the path to chromedriver executable by the `--chromedriver` argument from cli.)


## Build from source

Crone this repo, and run:

```bash
pip install --upgrade setuptools build
python -m build
pip install .\dist\peatix_cli-0.0.1-py3-none-any.whl
```

# Development

```bash
pip install -r requirements.txt
pip install -e .
```
