from rich import print as pprint
import argparse

banner = r"""
████████╗██╗   ██╗██████╗ ██████╗  ██████╗        ██████╗ █████╗ ███████╗███████╗
╚══██╔══╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗      ██╔════╝██╔══██╗██╔════╝██╔════╝
   ██║   ██║   ██║██████╔╝██████╔╝██║   ██║█████╗██║     ███████║███████╗█████╗  
   ██║   ██║   ██║██╔══██╗██╔══██╗██║   ██║╚════╝██║     ██╔══██║╚════██║██╔══╝  
   ██║   ╚██████╔╝██║  ██║██████╔╝╚██████╔╝      ╚██████╗██║  ██║███████║███████╗
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝        ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝
"""


def get_version():  # TODO: find a better way to get the version (maybe from setup.py)
    return "0.0.1"


def print_banner():
    """Print banner and version"""
    msg1_raw = get_version()
    msg2_raw = "made with :white_heart: by @Ahmad-Alsaleh"

    full_msg_raw = f"{msg1_raw} - {msg2_raw}"
    full_msg_colored = f"[bold][cyan]v{msg1_raw}[/cyan] - [red]{msg2_raw}[/red]\n"

    padding = len(banner.splitlines()[1]) // 2 - len(full_msg_raw) // 2

    pprint(f"[yellow]{banner}")
    pprint(" " * padding, full_msg_colored, sep="")


class CustomHelpFormatter(argparse.HelpFormatter):
    def format_help(self) -> str:
        return (
            super()
            .format_help()
            .replace("usage:", "Usage:")
            .replace("options:", "Options:")
        )
