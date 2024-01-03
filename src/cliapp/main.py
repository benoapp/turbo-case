import argparse
import utility
from TestManagementSystems.Factory import Factory
from rich import print as pprint

HELP_MESSAGE = "Show help"


def create_main_and_sub_parsers():
    parser = argparse.ArgumentParser(
        prog="turbocase",
        description="Turbo-Case: a helper CLI App that enables manual-test-as-code",
        add_help=False,
        formatter_class=utility.CustomHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="selected_command",
        metavar="<command>",
        help="Use '%(prog)s <command> --help' for more information",
    )

    return parser, subparsers


def add_global_options(parser: argparse.ArgumentParser):
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


def add_create_command(subparsers: argparse._SubParsersAction):
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


def handle_create_command(args):
    created_files_n = 0
    for file_path in args.files:
        try:
            test_management_system = Factory.get_test_management_system(args.system)
            test_management_system.create_test_case(file_path, args.api_key)
            created_files_n += 1
        except Exception as e:
            pprint(
                f"[red][ERR] Failed to create test case from file: [yellow]`{file_path}`[/yellow]. Reason:\n{e}\n"
            )

    test_case_plural = "s" if len(args.files) > 1 else ""
    pprint(
        f"[green]Created [cyan]{created_files_n}/{len(args.files)}[/cyan] test case{test_case_plural}."
    )


def add_update_command(subparsers: argparse._SubParsersAction):
    update_parser = subparsers.add_parser(
        "update",
        help="Override existing test cases (search by ID)",
        description="Override existing test cases (search by ID)",
        add_help=False,
        formatter_class=utility.CustomHelpFormatter,
    )

    update_parser.add_argument(
        "files",
        help="Paths of (YAML) test files",
        metavar="<file>",
        nargs="+",
    )

    update_parser.add_argument(
        "-s",
        "--system",
        default="Testiny",
        help="Test management system. Default: Testiny. Options: Testiny",
        metavar="<system>",
        choices=["Testiny"],
    )

    update_parser.add_argument(
        "-k",
        "--api-key",
        required=True,
        metavar="<key>",
        help="API key",
    )

    update_parser.add_argument(
        "-i",
        "--id",
        required=True,
        metavar="<id>",
        type=int,
        help="Test case ID",
    )

    update_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )


def handle_update_command(args):
    pass  # todo

def parse_args(parser: argparse.ArgumentParser):
    args = parser.parse_args()

    if args.selected_command is None:
        utility.print_banner()
        parser.print_help()

    if args.selected_command == "create":
        handle_create_command(args)


def main():
    parser, subparsers = create_main_and_sub_parsers()

    add_global_options(parser)

    add_create_command(subparsers)

    add_update_command(subparsers)

    parse_args(parser)


if __name__ == "__main__":
    main()
