import argparse
from typing import Any
from requests import HTTPError
import toml
import os
from .__init__ import __version__
from rich.console import Console

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


def print_banner():
    """Print the banner and version of turbocase."""
    console = Console(width=len(BANNER.splitlines()[1]))
    console.print(f"[yellow]{BANNER}")
    console.print(
        f"[bold][cyan]v{__version__}[/cyan] - [red]made with :white_heart: by @Ahmad-Alsaleh[/red]",
        justify="center",
    )
    console.rule(style="cyan", characters="═")


def get_configuration(configuration_name: str) -> Any:
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


def print_error_hints(e: Exception, *, console: Console):
    if isinstance(e, HTTPError) and e.response is not None:
        if e.response.status_code == 403:
            console.print(ERROR_403_HINT)
        elif e.response.status_code == 404:
            console.print(ERROR_404_HINT)
