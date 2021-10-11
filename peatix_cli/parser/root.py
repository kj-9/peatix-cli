import argparse
from pathlib import Path

from peatix_cli.command.search import SearchCmd

parser = argparse.ArgumentParser(
    prog='peatix',
    description='Search and featch peatix events.',
)

subparsers = parser.add_subparsers(required=True,
                                   title='subcommands')


parser_search = subparsers.add_parser(
    'search', help='Search events and output a result table')


parser_search.add_argument(
    '--chromedriver',
    type=Path,
    default=None,
    help='path to chromedriver executable')

parser_search.add_argument(
    '--max_page',
    type=int,
    default=30,
    help='miximum number of pages to featch results,  (default: %(default)s)')

parser_search.add_argument(
    '--period',
    type=str,
    choices=['today', 'this_weekend', 'next_week', ''],
    default='this_weekend',
    help='filter if date of events is in period, set \'\' to not to filter, (default: %(default)s)'
)

parser_search.add_argument(
    '--show_link',
    action='store_true',
    help='if this flag is set, show a bare url link instead of an embedded link')

parser_search.add_argument(
    '--tag_id',
    type=int,
    default='',
    help='filter by tag_id, , set \'\' to not to filter, (default: %(default)s)')


def run(args):
    SearchCmd(args).run()


parser_search.set_defaults(func=run)
