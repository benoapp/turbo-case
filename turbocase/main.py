import argparse
from rich_argparse import RichHelpFormatter, HelpPreviewAction
import toml
import os
from rich.console import Console
from turbocase.enums import App, Project
from turbocase.utility import (
    HINT_PREFIX,
    file_exists_in_project,
    print_banner,
    print_error_hints,
    get_result_color,
    CONFIG_FILE_PATH,
)
from turbocase.__init__ import __version__
from turbocase.Testiny import Testiny

HELP_MESSAGE = "Show help"
SUCCESS_PREFIX = ":heavy_check_mark:"
FAILURE_PREFIX = "[bold][ERR][/bold]"

# changing style of `back tick quoted text` in help messages
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
        help="Create new test cases or update existing ones (based on Title matching)",
        description="Create new test cases or update existing ones (based on Title matching)",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )

    upsert_parser.add_argument(
        "-p",
        "--project-path",
        help="Path of the project. Default: current directory",
        metavar="<project_path>",
        default=".",
    )

    upsert_parser.add_argument(
        "-a",
        "--app",
        choices=[app.value.name for app in App],
        help=f"The type of the app. Choose from: {', '.join([app.value.name for app in App])}. Default: app",
        metavar="<target_app>",
        default="app",
    )

    upsert_parser.add_argument(
        "test_titles",
        help="The title of the test case",
        metavar="<test_title>",
        nargs="+",
    )

    upsert_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )


def handle_upsert_command(args: argparse.Namespace, *, console: Console):
    """
    Handles the upsert command by calling the appropriate Testiny method.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    upserted_files_n = 0
    for test_title in args.test_titles:
        console.rule(f"[cyan]Test Case: [yellow]`{test_title}`[/yellow]")
        try:
            upsert_operation, test_cases_ids = Testiny.upsert_test_case(
                test_title, App[args.app.upper()], args.project_path
            )

            formatted_ids = ", ".join(
                [f"{id} ({project.name} project)" for id, project in test_cases_ids]
            )

            console.print(
                f"[green]{SUCCESS_PREFIX} Successfully upserted test case "
                f"with ID: [yellow]`{formatted_ids}`[/yellow]. Operation: [yellow]`{upsert_operation.name}`[/yellow]."
            )
            upserted_files_n += 1
        except Exception as e:
            console.print(
                f"[red]{FAILURE_PREFIX} Failed to upsert test case from file: "
                f"[yellow]`{test_title}[/yellow]. Reason:\n[dark_orange]{e}"
            )
            print_error_hints(e, console=console)
        console.print()  # cosmetic
    if len(args.test_titles) > 1:
        console.rule("[cyan]Results", characters="═")
        color = get_result_color(upserted_files_n, len(args.test_titles))
        console.print(
            f"[{color.value}]Upserted [cyan]{upserted_files_n}/{len(args.test_titles)}[/cyan] test cases."
        )


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


def add_init_command(subparsers: argparse._SubParsersAction):
    """
    Add the 'init' command to the subparsers.

    Args:
        subparsers (argparse._SubParsersAction): The subparsers object to add the command to.
    """
    init_parser = subparsers.add_parser(
        "init",
        help="Create an empty Git repository or reinitialize an existing one",
        description="Create an empty test management project repository or reinitialize an existing one",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )

    init_parser.add_argument(
        "directory",
        help="Path of the project. Default: current directory.",
        metavar="<director>",
        nargs="?",
        default=".",
    )

    init_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )


def handle_init_command(args: argparse.Namespace, *, console: Console):
    """
    Handles the 'int' command by creating folders and files for the project.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        console (Console): The rich console object.

    Returns:
        None
    """
    try:
        os.chdir(args.directory)
        projects_ids = dict()
        for project in Project:
            while True:
                full_project_name = console.input(
                    f"[green]Enter the full project name of the [yellow]`{project.name}`[/yellow] App in Testiny: "
                )
                project_id = Testiny.get_project_id(full_project_name)
                if project_id:
                    break
                else:
                    console.print(
                        f"[red]{FAILURE_PREFIX} No project found with the given name. Try again."
                    )
            projects_ids[project.name] = project_id
            console.print(
                f"[green]{SUCCESS_PREFIX} Project found with ID: [yellow]`{project_id}`[/yellow]."
            )
            console.print()  # cosmetic

        for app in App:
            os.makedirs(app.value.path, exist_ok=True)

        os.makedirs(".turbocase", exist_ok=True)
        with open(".turbocase/project.toml", "w") as project_file:
            toml.dump(projects_ids, project_file)

        console.rule("[cyan]Results", characters="═", style="cyan")
        console.print(f"[green]{SUCCESS_PREFIX} Successfully initialized project.")
    except Exception as e:
        console.print(
            f"[red]{FAILURE_PREFIX} Failed to create project. Reason:\n[dark_orange]{e}"
        )
        print_error_hints(e, console=console)


def add_generate_command(subparsers: argparse._SubParsersAction):
    """
    Add the 'generate' command to the subparsers.

    Args:
        subparsers (argparse._SubParsersAction): The subparsers object to add the command to.
    """
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate test case template",
        description="Generate test case template",
        add_help=False,
        formatter_class=RichHelpFormatter,
    )

    generate_parser.add_argument(
        "app",
        choices=[app.value.name for app in App],
        help=f"The type of the app. Choose from: {', '.join([app.value.name for app in App])}.",
        metavar="<target_app>",
    )

    generate_parser.add_argument(
        "test_title",
        help="The title of the test case",
        metavar="<test_title>",
    )

    generate_parser.add_argument(
        "project_path",
        help="Path of the project. Default: current directory",
        metavar="<project_path>",
        nargs="?",
        default=".",
    )

    generate_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help=HELP_MESSAGE,
    )


def handle_generate_command(args: argparse.Namespace, *, console: Console):
    """
    Handles the 'generate' command by creating a test case template in the corresponding app folder.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        console (Console): The rich console object.

    Returns:
        None
    """
    try:
        if not os.path.exists(
            os.path.join(args.project_path, ".turbocase/project.toml")
        ):
            console.print(
                f"[red]{FAILURE_PREFIX} No project found in the given path. "
                "Run [yellow]`turbocase project --help`[/yellow] "
                "for more information on how to initialize a project."
            )
            exit(1)

        folder = file_exists_in_project(f"{args.test_title}.yaml", args.project_path)
        if folder:
            console.print(
                f"[red]{FAILURE_PREFIX} Test case with the given title already exists in the project (Under `{folder}`).\n"
                f"{HINT_PREFIX} Consider using the app and/or project names in the title to avoid conflicts."
            )
            exit(1)

        template = Testiny.generate_test_case_template()

        full_template_path = os.path.join(
            args.project_path,
            App[args.app.upper()].value.path,
            f"{args.test_title}.yaml",
        )
        if not os.path.exists(os.path.dirname(full_template_path)):
            console.print(
                f"[red]{FAILURE_PREFIX} Project folder is corrupted. "
                "Run [yellow]`turbocase project --help`[/yellow] "
                "for more information on how to re-initialize the project."
            )
            exit(1)

        with open(full_template_path, "w") as template_file:
            template_file.write(template)

        console.print(
            f"[green]{SUCCESS_PREFIX} Successfully generated test case template."
        )
    except Exception as e:
        console.print(
            f"[red]{FAILURE_PREFIX} Failed to generate test case template. Reason:\n[dark_orange]{e}"
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

    elif args.selected_command == "read":
        with console.status("[bold green]Reading test case..."):
            handle_read_command(args, console=console)

    elif args.selected_command == "upsert":
        with console.status("[bold green]Upserting test cases..."):
            handle_upsert_command(args, console=console)

    elif args.selected_command == "config":
        with console.status("[bold green]Configuring Turbo-Case..."):
            handle_config_command(args, console=console)

    elif args.selected_command == "init":
        handle_init_command(args, console=console)

    elif args.selected_command == "generate":
        handle_generate_command(args, console=console)


def main():
    parser, subparsers = create_main_and_sub_parsers()

    add_global_options(parser)

    add_init_command(subparsers)

    add_config_command(subparsers)

    add_generate_command(subparsers)

    add_upsert_command(subparsers)

    add_read_command(subparsers)

    parse_args(parser)


if __name__ == "__main__":
    main()
