from enum import Enum
from typing import Any
from requests import HTTPError
from rich.console import Console
import toml
import os
from .__init__ import __version__

HINT_PREFIX = "[blue][bold]Hint:[/bold]"
ERROR_404_HINT = (
    f"{HINT_PREFIX} Are you sure you used the correct test case ID?\n"
    f"{HINT_PREFIX} Are you sure the project ID in the test case file is accurate?"
)
ERROR_403_HINT = f"{HINT_PREFIX} Are you sure you used the correct API key? Try [yellow]`turbocase config --help`[/yellow]."

CONFIG_FILE_PATH = os.path.expanduser("~/.turbocase.toml")

BANNER = r"""
████████╗██╗   ██╗██████╗ ██████╗  ██████╗        ██████╗ █████╗ ███████╗███████╗
╚══██╔══╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗      ██╔════╝██╔══██╗██╔════╝██╔════╝
   ██║   ██║   ██║██████╔╝██████╔╝██║   ██║█████╗██║     ███████║███████╗█████╗  
   ██║   ██║   ██║██╔══██╗██╔══██╗██║   ██║╚════╝██║     ██╔══██║╚════██║██╔══╝  
   ██║   ╚██████╔╝██║  ██║██████╔╝╚██████╔╝      ╚██████╗██║  ██║███████║███████╗
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝        ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝
"""


class Color(Enum):
    """The color of the result."""

    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"


class Project(Enum):
    """
    Enum representing the project to which the test case belongs.

    Possible values:
    - IOS: Indicates that the test case belongs to the iOS project.
    - ANDROID: Indicates that the test case belongs to the Android project.
    - WEB: Indicates that the test case belongs to the Web project.
    """

    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


def print_banner():
    """Print the banner and version of turbocase."""
    console = Console(width=len(BANNER.splitlines()[1]))
    console.print(f"[yellow]{BANNER}")
    console.print(
        f"[bold][cyan]v{__version__}[/cyan] - [red]made with :white_heart: by @Ahmad-Alsaleh[/red]",
        justify="center",
    )
    console.rule(style="cyan", characters="═")


def get_turbocase_configuration(configuration_name: str) -> Any:
    """
    Retrieve the value of a configuration from the ~/.turbocase.toml file.

    Args:
        configuration_name (str): The name of the configuration to retrieve.

    Returns:
        Any: The value of the configuration.

    Raises:
        KeyError: If the configuration does not exist in the file.
            This can happen if the file is corrupted.
    """
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_file:
        configurations = toml.load(config_file)
        try:
            return configurations[configuration_name]
        except KeyError:
            raise KeyError(
                "Config file is corrupted. "
                "Run [yellow]`turbocase config --api-key <YOUR_API_KEY>`[/yellow] to fix it.\n"
                "See [yellow]`turbocase config --help`[/yellow] for more information."
            )


def get_project_id(project: Project, project_path: str) -> int:
    """
    Get the project ID for a given sub-app from the .project.toml file.

    Args:
        sub_app (str): The sub-app name (ios, android, or web).
        project_path (str): The path to the project folder.

    Returns:
        int: The project ID.

    Raises:
        KeyError: If the sub-app is not found in the project configurations.
    """
    project_config_file_path = os.path.join(project_path, ".project.toml")
    with open(project_config_file_path, "r") as project_config_file:
        configurations = toml.load(project_config_file)
        try:
            return configurations[project.value]
        except KeyError:
            raise KeyError(
                "Project folder is corrupted. "
                "Run [yellow]`turbocase project --help`[/yellow] for more information "
                "on how to fix it.\n"
            )


def print_error_hints(e: Exception, *, console: Console):
    if isinstance(e, HTTPError) and e.response is not None:
        if e.response.status_code == 403:
            console.print(ERROR_403_HINT)
        elif e.response.status_code == 404:
            console.print(ERROR_404_HINT)


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
