import argparse
from rich import print as pprint
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
