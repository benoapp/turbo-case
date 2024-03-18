from typing import Any
from requests import HTTPError
from rich.console import Console
import toml
import os
from turbocase.__init__ import __version__
from turbocase.enums import Color, Project

HINT_PREFIX = "[blue][bold]Hint:[/bold]"
SUCCESS_PREFIX = ":heavy_check_mark:"
FAILURE_PREFIX = "[bold][ERR][/bold]"

BANNER = r"""
████████╗██╗   ██╗██████╗ ██████╗  ██████╗        ██████╗ █████╗ ███████╗███████╗
╚══██╔══╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗      ██╔════╝██╔══██╗██╔════╝██╔════╝
   ██║   ██║   ██║██████╔╝██████╔╝██║   ██║█████╗██║     ███████║███████╗█████╗  
   ██║   ██║   ██║██╔══██╗██╔══██╗██║   ██║╚════╝██║     ██╔══██║╚════██║██╔══╝  
   ██║   ╚██████╔╝██║  ██║██████╔╝╚██████╔╝      ╚██████╗██║  ██║███████║███████╗
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝        ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝
"""


class NotTurboCaseProject(Exception):
    """Base class for all TurboCase exceptions."""

    def __init__(self, message: str | None = None):
        if message is None:
            self.message = (
                "Could not find a [yellow]`.turbocase`[/yellow] folder. "
                "Are you sure you are in a TurboCase project folder?"
            )
        else:
            self.message = message
        super().__init__(self.message)


def print_banner():
    """Print the banner and version of turbocase."""
    console = Console(width=len(BANNER.splitlines()[1]))
    console.print(f"[yellow]{BANNER}")
    console.print(
        f"[bold][cyan]v{__version__}[/cyan] - [red]made with :white_heart: by @Ahmad-Alsaleh[/red]",
        justify="center",
    )
    console.rule(style="cyan", characters="═")


def get_turbocase_folder_path(*, __current_dir: str | None = None) -> str:
    """
    Get the path to the .turbocase folder of a turbocase project.

    Returns:
        str: The path to the .turbocase folder.
    """
    if __current_dir is None:
        __current_dir = os.getcwd()

    turbocase_folder_path = os.path.join(__current_dir, ".turbocase")
    if os.path.exists(turbocase_folder_path):
        return turbocase_folder_path

    if os.path.ismount(__current_dir) or __current_dir == "/":
        raise NotTurboCaseProject()

    return get_turbocase_folder_path(__current_dir=os.path.dirname(__current_dir))


def get_project_configuration(configuration_name: str) -> Any:
    """
    Retrieve the value of a project configuration from the .turbocase/project.toml file.

    Args:
        configuration_name (str): The name of the configuration to retrieve.

    Returns:
        Any: The value of the configuration.

    Raises:
        KeyError: If the configuration does not exist in the file.
            This can happen if the file is corrupted.
    """
    config_file_path = os.path.join(get_turbocase_folder_path(), "project.toml")
    with open(config_file_path, "r") as config_file:
        configurations = toml.load(config_file)
        try:
            return configurations[configuration_name]
        except KeyError:
            raise KeyError(
                "Turbocase folder is corrupted. Use [yellow]`turbocase init`[/yellow] to reinitialize it."
            )


def get_project_id(project: Project, project_path: str) -> int:
    """
    Get the project ID for a given sub-app from the .turbocase/project.toml file.

    Args:
        project (Project): The project for which to retrieve the project ID.
        project_path (str): The path to the project folder.

    Returns:
        int: The project ID.

    Raises:
        KeyError: If the sub-app is not found in the project configurations.
    """
    project_config_file_path = os.path.join(project_path, ".turbocase/project.toml")
    with open(project_config_file_path, "r") as project_config_file:
        configurations = toml.load(project_config_file)
        try:
            return configurations[project.name]
        except KeyError:
            raise KeyError(
                "Project folder is corrupted. "
                "Run [yellow]`turbocase project --help`[/yellow] for more information "
                "on how to re-initialize the project."
            )


def print_error_hints(e: Exception, *, console: Console) -> None:
    """
    Prints error hints based on the type of exception.

    Args:
        e (Exception): The exception that occurred.
        console (Console): The console object used for printing.
    """
    if isinstance(e, HTTPError):
        if e.response.status_code == 403:
            console.print(
                f"{HINT_PREFIX} Use [yellow]`turbocase init`[/yellow] to initialize a new project."
            )
        elif e.response.status_code == 404:
            console.print(
                f"{HINT_PREFIX} Are you sure you used the correct test case ID?"
            )
    elif isinstance(e, NotTurboCaseProject):
        console.print(
            f"{HINT_PREFIX} Use [yellow]`turbocase init`[/yellow] to initialize a new project."
        )


def get_result_color(created_files_n: int, file_n: int) -> Color:
    """
    Determines the color of the result based on the number of created files and the total number of files.

    Args:
        created_files_n (int): The number of files that were successfully created.
        file_n (int): The total number of files.

    Returns:
        Color: The color of the result (RED, GREEN, or YELLOW).
    """
    if created_files_n == file_n:
        return Color.GREEN
    elif created_files_n == 0:
        return Color.RED
    else:
        return Color.YELLOW


def file_exists_in_project(file_name, project_path) -> str | None:
    """
    Check if a file exists in a project folder.

    Args:
        file_name (str): The name of the file to check.
        project_folder_path (str): The path to the project folder.

    Returns:
        str | None: The name of the folder where the file exists, or None if the file is not found.
    """
    for root, _, files in os.walk(os.path.join(project_path, "app")):
        if file_name in files:
            return os.path.basename(root)
    return None
