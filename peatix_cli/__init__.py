from peatix_cli.main import Main
from peatix_cli.parser import parser


def run():

    args = parser.parse_args()
    Main(args).run()
