from rich import print as pprint
import argparse
import os
import toml

BANNER = r"""
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

    padding = len(BANNER.splitlines()[1]) // 2 - len(full_msg_raw) // 2

    pprint(f"[yellow]{BANNER}")
    pprint(" " * padding, full_msg_colored, sep="")


class CustomHelpFormatter(argparse.HelpFormatter):
    def format_help(self) -> str:
        return (
            super()
            .format_help()
            .replace("usage:", "Usage:")
            .replace("options:", "Options:")
            .replace("positional arguments:", "Arguments:")
        )


# ! move to main
def handle_setup(api_key: str):
    file_path = os.path.join(
        os.path.expanduser("~"), ".config", "turbocase", "settings.toml"
    )
    if not os.path.isfile(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            toml.dump(
                {
                    "test_management_system": {
                        "default": "Testiny",
                    },
                    "api": {
                        "key": api_key,
                    },
                    "user": {  # ! issue: uncouple with Testiny class
                        "ID": Testiny.get_user_id(api_key),
                    },
                },
                file,
            )
