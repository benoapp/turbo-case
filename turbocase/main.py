import argparse
from rich_argparse import RichHelpFormatter, HelpPreviewAction
import toml
import os
from rich.console import Console
from .utility import print_banner, print_error_hints, CONFIG_FILE_PATH
from .__init__ import __version__
from .Testiny import Testiny

HELP_MESSAGE = "Show help"
SUCCESS_PREFIX = ":heavy_check_mark:"
FAILURE_PREFIX = "[bold][ERR][/bold]"

# change style of `back tick quoted text` in help messages
RichHelpFormatter.styles["argparse.syntax"] = "bold yellow"

RichHelpFormatter.styles["argparse.prog"] = "bold yellow"


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
        formatter_class=RichHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="selected_command",
        metavar="<command>",
        help="Use `%(prog)s <command> --help` for more information",
    )

    # this action is hidden from the help message
    parser.add_argument(
        "--generate-turbocase-preview",
        action=HelpPreviewAction,
        path="assets/turbocase-preview.svg",
    )

    return parser, subparsers


def add_global_options(parser: argparse.ArgumentParser):
    """
    Add global options to the argument parser.

    Args:
        parser (argparse.ArgumentParser): The main argument parser to add options to.
    """

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"[yellow]%(prog)s [cyan]v{__version__}",
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
        formatter_class=RichHelpFormatter,
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


def handle_create_command(args: argparse.Namespace, *, console: Console):
    """
    Handles the 'create' command by creating test cases using the specified test management system.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    created_files_n = 0
    for file_path in args.files:
        console.rule(f"[cyan]Test Case File: [yellow]`{file_path}`[/yellow]")
        try:
            test_case_id = Testiny.create_test_case(file_path)
            console.print(
                f"[green]{SUCCESS_PREFIX} Successfully created test case "
                f"with ID [yellow]`{test_case_id}`[/yellow]."
            )
            created_files_n += 1
        except Exception as e:
            console.print(
                f"[red]{FAILURE_PREFIX} Failed to create test case from file: "
                f"[yellow]`{file_path}`[/yellow]. Reason:\n[dark_orange]{e}"
            )
            print_error_hints(e, console=console)
        console.print()  # cosmetic
    if len(args.files) > 1:
        console.print("[cyan]Done")
        console.print(
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
        formatter_class=RichHelpFormatter,
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


def handle_update_command(args: argparse.Namespace, *, console: Console):
    """
    Handles the 'update' command by updating a test case in the test management system.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    try:
        Testiny.update_test_case(args.file, args.id)
        console.print(
            f"[green]{SUCCESS_PREFIX} Successfully updated test case with ID: "
            f"[yellow]`{args.id}`[/yellow]."
        )
    except Exception as e:
        console.print(
            f"[red]{FAILURE_PREFIX} Failed to update test case with ID: "
            f"[yellow]`{args.id}`[/yellow]. Reason:\n[dark_orange]{e}"
        )
        print_error_hints(e, console=console)


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
        formatter_class=RichHelpFormatter,
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


def handle_read_command(args: argparse.Namespace, *, console: Console):
    """
    Handles the 'read' command by retrieving and printing information about a test case.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    try:
        test_case = Testiny.read_test_case(args.id)
        console.print(test_case)
    except Exception as e:
        console.print(
            f"[red]{FAILURE_PREFIX} Failed to read test case with ID: "
            f"[yellow]`{args.id}`[/yellow]. Reason:\n[dark_orange]{e}"
        )
        print_error_hints(e, console=console)


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
        formatter_class=RichHelpFormatter,
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


def handle_upsert_command(args: argparse.Namespace, *, console: Console):
    """
    Handles the upsert command by calling the appropriate test management system's
    upsert_test_case method with the provided arguments.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    try:
        operation, test_case_id = Testiny.upsert_test_case(args.file)
        console.print(
            f"[green]{SUCCESS_PREFIX} Upsert successful for test case "
            f"[yellow]`{test_case_id}`[/yellow]. Operation: [yellow]`{operation.name}`[/yellow]."
        )
    except Exception as e:
        console.print(
            f"[red]{FAILURE_PREFIX} Failed to upsert test case. Reason:\n[dark_orange]{e}"
        )
        print_error_hints(e, console=console)


def add_config_command(subparsers: argparse._SubParsersAction):
    """
    Add the 'config' command to the subparsers.

    Args:
        subparsers (argparse._SubParsersAction): The subparsers object to add the command to.
    """
    config_parser = subparsers.add_parser(
        "config",
        help="Configure Turbo-Case",
        description="Configure Turbo-Case",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )

    config_parser.add_argument(
        "-k",
        "--api-key",
        required=True,
        metavar="<key>",
        help="Testiny API key",
    )

    config_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )


def handle_config_command(args: argparse.Namespace, *, console: Console):
    """
    Handles the config command by configuring the Turbo-Case settings.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    try:
        configurations = {
            "api_key": args.api_key,
            "owner_user_id": Testiny.get_owner_user_id(args.api_key),
        }

        with open(CONFIG_FILE_PATH, "w") as config_file:
            toml.dump(configurations, config_file)

        console.print(
            f"[green]{SUCCESS_PREFIX} Successfully configured Turbo-Case.\n"
            f"Run [yellow]`turbocase --help`[/yellow] for more information on how to use turbocase."
        )
    except Exception as e:
        console.print(
            f"[red]{FAILURE_PREFIX} Failed to configure Turbo-Case. Reason:\n[dark_orange]{e}"
        )
        print_error_hints(e, console=console)


def parse_args(parser: argparse.ArgumentParser):
    """
    Parse the command line arguments and execute the corresponding command.

    Args:
        parser (argparse.ArgumentParser): The main argument parser object.

    Returns:
        None
    """
    args = parser.parse_args()
    console = Console()

    if not os.path.exists(CONFIG_FILE_PATH) and args.selected_command not in (
        "config",
        None,
    ):
        console.print(
            f"[red]{FAILURE_PREFIX} Configuration file not found. "
            f"Run [yellow]`turbocase config --api-key <YOUR_API_KEY>`[/yellow].\n"
            f"See [yellow]`turbocase config --help`[/yellow] for more information."
        )
        exit(1)

    if args.selected_command is None:
        print_banner()
        print()
        print(parser.format_help())

    elif args.selected_command == "create":
        with console.status("[bold green]Creating test cases..."):
            handle_create_command(args, console=console)

    elif args.selected_command == "read":
        with console.status("[bold green]Reading test case..."):
            handle_read_command(args, console=console)

    elif args.selected_command == "update":
        with console.status("[bold green]Updating test case..."):
            handle_update_command(args, console=console)

    elif args.selected_command == "upsert":
        with console.status("[bold green]Upserting test case..."):
            handle_upsert_command(args, console=console)

    elif args.selected_command == "config":
        with console.status("[bold green]Configuring Turbo-Case..."):
            handle_config_command(args, console=console)


def main():
    parser, subparsers = create_main_and_sub_parsers()

    add_global_options(parser)

    add_config_command(subparsers)

    add_upsert_command(subparsers)

    add_create_command(subparsers)

    add_update_command(subparsers)

    add_read_command(subparsers)

    parse_args(parser)


if __name__ == "__main__":
    main()
