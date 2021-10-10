from peatix_cli.parser.root import parser


def run():

    args = parser.parse_args()
    args.func(args)
