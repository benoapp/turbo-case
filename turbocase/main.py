import argparse
from rich import print as pprint
from requests.exceptions import HTTPError
from .utility import print_banner, CustomHelpFormatter
from .__init__ import __version__
from .Testiny import Testiny

HELP_MESSAGE = "Show help"
SUCCESS_PREFIX = ":heavy_check_mark:"
FAILURE_PREFIX = "[bold][ERR][/bold]"
HINT_PREFIX = "[blue][bold]Hint:[/bold]"
ERROR_404_HINT = f"{HINT_PREFIX} Are you sure you used the correct test case ID?"
ERROR_403_HINT = (
    f"{HINT_PREFIX} Are you sure you used the correct API key?\n"
    f"{HINT_PREFIX} Are you sure the project ID in the test case file is accurate?"
)


def create_main_and_sub_parsers():
    """
    Create the main parser and subparsers for the Turbo-Case CLI app.

    Returns:
        parser (argparse.ArgumentParser): The main parser object.
        subparsers (argparse._SubParsersAction): The subparsers object.
    """
    parser = argparse.ArgumentParser(
        prog="turbocase",
        description="Turbo-Case: a helper CLI App that enables manual-test-as-code",
        add_help=False,
        formatter_class=CustomHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="selected_command",
        metavar="<command>",
        help="Use '%(prog)s <command> --help' for more information",
    )

    return parser, subparsers


def add_global_options(parser: argparse.ArgumentParser):
    """
    Add global options to the argument parser.

    Args:
        parser (argparse.ArgumentParser): The main argument parser to add options to.
    """
    parser.add_argument(
        "-k",
        "--api-key",
        required=True,
        metavar="<key>",
        help="API key",
    )

    parser.add_argument(
        "-s",
        "--system",
        default="Testiny",
        help="Test management system. Default: Testiny. Options: Testiny",
        metavar="<system>",
        choices=["Testiny"],
    )

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{__version__}",
        help="Show program's version",
    )


def add_create_command(subparsers: argparse._SubParsersAction):
    """
    Add the 'create' command to the subparsers.

    Args:
        subparsers (argparse._SubParsersAction): The subparsers object to add the command to.
    """
    create_parser = subparsers.add_parser(
        "create",
        help="Create test cases from YAML files",
        description="Create test cases from YAML files",
        add_help=False,
        formatter_class=CustomHelpFormatter,
    )

    create_parser.add_argument(
        "files",
        help="Paths of (YAML) test files",
        metavar="<file>",
        nargs="+",
    )

    create_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )


def handle_create_command(args: argparse.Namespace):
    """
    Handles the 'create' command by creating test cases using the specified test management system.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    created_files_n = 0
    for file_path in args.files:
        try:
            test_case_id = Testiny.create_test_case(file_path)
            pprint(
                f"[green]{SUCCESS_PREFIX} Successfully created test case "
                f"[yellow]`{test_case_id}`[/yellow] from file: [yellow]`{file_path}`[/yellow]."
            )
            created_files_n += 1
        except Exception as e:
            pprint(
                f"[red]{FAILURE_PREFIX} Failed to create test case from file: "
                f"[yellow]`{file_path}`[/yellow]. Reason:\n[dark_orange]{e}"
            )
    if len(args.files) > 1:
        pprint(
            f"[green]Created [cyan]{created_files_n}/{len(args.files)}[/cyan] test cases."
        )


def add_update_command(subparsers: argparse._SubParsersAction):
    """
    Add the 'update' command to the subparsers.

    Args:
        subparsers (argparse._SubParsersAction): The subparsers object to add the command to.
    """
    update_parser = subparsers.add_parser(
        "update",
        help="Overwrite existing test cases (based on ID matching)",
        description="Overwrite existing test cases (based on ID matching)",
        add_help=False,
        formatter_class=CustomHelpFormatter,
    )

    update_parser.add_argument(
        "file",
        help="Path of (YAML) test file",
        metavar="<file>",
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


def handle_update_command(args: argparse.Namespace):
    """
    Handles the 'update' command by updating a test case in the test management system.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    try:
        Testiny.update_test_case(args.file, args.id)
        pprint(
            f"[green]{SUCCESS_PREFIX} Successfully updated test case with ID: "
            f"[yellow]`{args.id}`[/yellow]."
        )
    except Exception as e:
        pprint(
            f"[red]{FAILURE_PREFIX} Failed to update test case with ID: "
            f"[yellow]`{args.id}`[/yellow]. Reason:\n[dark_orange]{e}"
        )
        if isinstance(e, HTTPError) and e.response.status_code == 404:
            pprint(ERROR_404_HINT)


def add_read_command(subparsers: argparse._SubParsersAction):
    """
    Add the 'read' command to the subparsers.

    Args:
        subparsers (argparse._SubParsersAction): The subparsers object to add the command to.
    """
    read_parser = subparsers.add_parser(
        "read",
        help="Read existing test cases (search by ID)",
        description="Read existing test cases (search by ID)",
        add_help=False,
        formatter_class=CustomHelpFormatter,
    )

    read_parser.add_argument(
        "-i",
        "--id",
        required=True,
        metavar="<id>",
        type=int,
        help="Test case ID",
    )

    read_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )


def handle_read_command(args: argparse.Namespace):
    """
    Handles the 'read' command by retrieving and printing information about a test case.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    try:
        test_case_info = Testiny.read_test_case(args.id)
        pprint(test_case_info)
    except Exception as e:
        pprint(
            f"[red]{FAILURE_PREFIX} Failed to read test case with ID: "
            f"[yellow]`{args.id}`[/yellow]. Reason:\n[dark_orange]{e}"
        )
        if isinstance(e, HTTPError):
            if e.response.status_code == 403:
                pprint(ERROR_403_HINT)
            elif e.response.status_code == 404:
                pprint(ERROR_404_HINT)


def add_upsert_command(subparsers: argparse._SubParsersAction):
    """
    Add the 'upsert' command to the subparsers.

    Args:
        subparsers (argparse._SubParsersAction): The subparsers object to add the command to.
    """
    upsert_parser = subparsers.add_parser(
        "upsert",
        help="Create a new test case or update an existing one (based on Title matching)",
        description="Create a new test case or update an existing one (based on Title matching)",
        add_help=False,
        formatter_class=CustomHelpFormatter,
    )

    upsert_parser.add_argument(
        "file",
        help="Path of (YAML) test file",
        metavar="<file>",
    )

    upsert_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )


def handle_upsert_command(args: argparse.Namespace):
    """
    Handles the upsert command by calling the appropriate test management system's
    upsert_test_case method with the provided arguments.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    try:
        test_management_system = get_test_management_system(args.system)
        operation, test_case_id = test_management_system.upsert_test_case(
            args.file, args.api_key
        )
        pprint(
            f"[green]{SUCCESS_PREFIX} Upsert successful for test case "
            f"[yellow]`{test_case_id}`[/yellow]. Operation: [yellow]`{operation.name}`[/yellow]."
        )
    except Exception as e:
        pprint(
            f"[red]{FAILURE_PREFIX} Failed to upsert test case. Reason:\n[dark_orange]{e}"
        )
        if isinstance(e, HTTPError) and e.response.status_code == 403:
            pprint(ERROR_403_HINT)


def parse_args(parser: argparse.ArgumentParser):
    """
    Parse the command line arguments and execute the corresponding command.

    Args:
        parser (argparse.ArgumentParser): The main argument parser object.

    Returns:
        None
    """
    args = parser.parse_args()

    if args.selected_command is None:
        print_banner()
        parser.print_help()

    elif args.selected_command == "create":
        handle_create_command(args)

    elif args.selected_command == "read":
        handle_read_command(args)

    elif args.selected_command == "update":
        handle_update_command(args)

    elif args.selected_command == "upsert":
        handle_upsert_command(args)


def main():
    parser, subparsers = create_main_and_sub_parsers()

    add_global_options(parser)

    add_create_command(subparsers)

    add_update_command(subparsers)

    add_read_command(subparsers)

    add_upsert_command(subparsers)

    parse_args(parser)


if __name__ == "__main__":
    main()
