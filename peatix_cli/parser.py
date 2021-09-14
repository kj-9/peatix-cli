import argparse

from pathlib import Path

parser = argparse.ArgumentParser(
    prog='peatix_cli',
    description='Search and featch peatix events.',
)

parser.add_argument(
    '--chromedriver',
    required=True,
    type=Path,
    help='path to chromedriver executable')

parser.add_argument(
    '--max_page',
    type=int,
    default=30,
    help='miximum number of pages to featch results,  (default: %(default)s)')

parser.add_argument(
    '--filter',
    type=str,
    choices=['today', 'this_weekend', 'next_week', ''],
    default='this_weekend',
    help='filter to date of event, set \'\' to not to filter, (default: %(default)s)'
)
