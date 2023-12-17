import argparse
import utility
import TestSystem


def parse_args(parser: argparse.ArgumentParser):
    args = parser.parse_args()

    if not any(vars(args).values()):
        utility.print_banner()
        parser.print_help()

    if args.selected_command == "create":
        for file_path in args.files:
            TestSystem.get_test_system(args.system).create_test_case(
                file_path, args.api_key
            )


def main():
    HELP_MESSAGE = "Show help"

    # main- and sub-parsers
    parser = argparse.ArgumentParser(
        prog="turbocase",
        description="TurboCase is a helper CLI App that enables manual-test-as-code",
        add_help=False,
        usage="%(prog)s [command] [options]",
        formatter_class=utility.CustomHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="selected_command",
        metavar="<command>",
        help="Use '%(prog)s <command> --help' for more information",
    )

    # global arguments
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{utility.get_version()}",
        help="Show program's version",
    )

    # subparser for 'create' command
    create_parser = subparsers.add_parser(
        "create",
        help="Create test cases from YAML files",
        description="Create test cases from YAML files",
        add_help=False,
    )

    create_parser.add_argument(
        "files",
        help="Paths of (YAML) test files",
        nargs="+",
    )

    create_parser.add_argument(
        "-s",
        "--system",
        default="Testiny",
        help="Test management system. Default: Testiny. Options: Testiny",
        metavar="<system>",
        choices=["Testiny"],
    )

    create_parser.add_argument(
        "-k",
        "--api-key",
        required=True,
        metavar="<key>",
        help="API key",
    )

    create_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )

    parse_args(parser)


if __name__ == "__main__":
    main()
