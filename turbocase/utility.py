import argparse
from typing import Any
from rich import print as pprint
import toml
from .__init__ import __version__

BANNER = r"""
████████╗██╗   ██╗██████╗ ██████╗  ██████╗        ██████╗ █████╗ ███████╗███████╗
╚══██╔══╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗      ██╔════╝██╔══██╗██╔════╝██╔════╝
   ██║   ██║   ██║██████╔╝██████╔╝██║   ██║█████╗██║     ███████║███████╗█████╗  
   ██║   ██║   ██║██╔══██╗██╔══██╗██║   ██║╚════╝██║     ██╔══██║╚════██║██╔══╝  
   ██║   ╚██████╔╝██║  ██║██████╔╝╚██████╔╝      ╚██████╗██║  ██║███████║███████╗
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝        ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝
"""


def print_banner():
    """Print banner and version"""
    msg1_raw = __version__
    msg2_raw = "made with :white_heart: by @Ahmad-Alsaleh"

    full_msg_raw = f"{msg1_raw} - {msg2_raw}"
    full_msg_colored = f"[bold][cyan]v{msg1_raw}[/cyan] - [red]{msg2_raw}[/red]\n"

    padding = len(BANNER.splitlines()[1]) // 2 - len(full_msg_raw) // 2

    pprint(f"[yellow]{BANNER}")
    pprint(" " * padding, full_msg_colored, sep="")


class CustomHelpFormatter(argparse.HelpFormatter):
    """Custom help formatter for the command-line interface."""

    def format_help(self) -> str:
        """Format the help message with custom styling."""
        return (
            super()
            .format_help()
            .replace("usage:", "Usage:")
            .replace("options:", "Options:")
            .replace("positional arguments:", "Arguments:")
        )


def get_configuration(configuration_name: str) -> Any:
    """
    Retrieve the value of a configuration from the .turbocase.toml file.

    Args:
        configuration_name (str): The name of the configuration to retrieve.

    Returns:
        Any: The value of the configuration.

    Raises:
        KeyError: If the configuration does not exist in the file.
            This can happen if the file is corrupted.
    """
    with open(".turbocase.toml", "r", encoding="utf-8") as config_file:
        configurations = toml.load(config_file)
        try:
            return configurations[configuration_name]
        except KeyError:
            raise KeyError(
                "Config file is corrupted. "
                "Run [yellow]`turbocase config --api-key <YOUR_API_KEY>`[/yellow] to fix it.\n"
                "See [yellow]`turbocase config --help`[/yellow] for more information."
            )
