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


def get_banner():
    """Return banner and version string."""
    msg1_raw = __version__
    msg2_raw = "made with :white_heart: by @Ahmad-Alsaleh"

    full_msg_raw = f"{msg1_raw} - {msg2_raw}"
    full_msg_colored = f"[bold][cyan]v{msg1_raw}[/cyan] - [red]{msg2_raw}[/red]\n"

    padding = len(BANNER.splitlines()[1]) // 2 - len(full_msg_raw) // 2

    return f"[yellow]{BANNER}\n" + " " * padding + full_msg_colored


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
