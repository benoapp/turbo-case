from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class UpsertAction(Enum):
    """
    Enum representing the action to perform during an upsert operation.

    Possible values:
    - UPDATE: Indicates that the existing item was updated.
    - CREATE: Indicates that a new item was created.
    """

    UPDATE = auto()
    CREATE = auto()


class Color(Enum):
    """
    The color of the result.

    Possible values:
    - RED: Indicates 'none' test cases were created/updated successfully.
    - GREEN: Indicates 'all' test cases were created/updated successfully.
    - YELLOW: Indicates 'some' test cases were created/updated successfully.
    """

    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"


class Project(Enum):
    """
    Enum representing the project to which the test case belongs.

    Each of those projects maps directly to an existing project in Testiny.
    """

    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


@dataclass
class AppType:
    """
    Represents an App type.

    Attributes:
        name (str): The name of the app.
        path (str): The path of the app in the project folder.
        projects (List[Project]): The list of projects associated with the app.
    """

    name: str
    path: str
    projects: List[Project]


class App(Enum):
    IOS = AppType("ios", "app/mobile/ios", [Project.IOS])
    ANDROID = AppType("android", "app/mobile/android", [Project.ANDROID])
    MOBILE = AppType("mobile", "app/mobile", [Project.ANDROID, Project.IOS])
    WEB = AppType("web", "app/web", [Project.WEB])
    APP = AppType("app", "app", [Project.IOS, Project.ANDROID, Project.WEB])
