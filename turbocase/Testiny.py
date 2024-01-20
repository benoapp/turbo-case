from typing import Any, Tuple
from enum import Enum, auto
from urllib.parse import urljoin
import jsonschema
import requests
import yaml
import json
import os
from .utility import get_configuration


class UpsertAction(Enum):
    """
    Enum representing the action to perform during an upsert operation.

    Possible values:
    - UPDATE: Indicates that the existing item was updated.
    - CREATE: Indicates that a new item was created.
    """

    UPDATE = auto()
    CREATE = auto()


class Testiny:
    """
    A class representing the [Testiny](https://www.testiny.io/) test management system.
    """

    __CONTENT_TYPE = "application/json"
    __SCHEMA_FILE_PATH = os.path.join(
        os.path.dirname(__file__), "testiny_schema.json"
    )  # .todo: write this in a better (safer) way
    __API_URL = "https://app.testiny.io/api/v1/"

    @staticmethod
    def __read_test_case_file(file_path: str) -> Any:
        """Reads a test case file in YAML format and validates it against a JSON schema

        Args:
            file_path (str): The path to the test case file.

        Returns:
            Any: The loaded test case data.

        Raises:
            ValueError: If the file path does not refer to a valid YAML file.
        """
        if not file_path.endswith((".yaml", ".yml")):
            raise ValueError("File path does not refer to a valid YAML file")

        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        with open(Testiny.__SCHEMA_FILE_PATH, "r", encoding="utf-8") as schema_file:
            schema = json.load(schema_file)

        jsonschema.validate(data, schema)

        return data

    @staticmethod
    def __get_etag(test_case_id: int) -> str:
        """
        Get the ETag value for a given test case by reading it from the API.

        Args:
            test_case_id (int): The ID of the test case.

        Returns:
            str: The ETag value of the test case.
        """
        test_case = Testiny.__get_test_case_json(test_case_id)
        return test_case["_etag"]

    @staticmethod
    def __find_test_case_by_title(title: str) -> Tuple[int, str] | None:
        """Find a test case by its title.

        Args:
            title (str): The title of the test case.

        Returns:
            Tuple[int, str] | None: A tuple containing the ID and ETag of the test case if found,
            or None if no test case is found.

        Raises:
            ValueError: If more than one test case is found with the given title.
        """
        url = urljoin(Testiny.__API_URL, "testcase/find")
        payload = json.dumps({"filter": {"title": title}})
        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": get_configuration("api_key"),
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=10
        )
        response.raise_for_status()

        meta, data = response.json().values()
        if meta["count"] == 0:
            return None

        if meta["count"] > 1:
            raise ValueError(
                "More than one test case found with the given title. "
                "Please use the [yellow]`update`[/yellow] command."
            )

        return data[0]["id"], data[0]["_etag"]

    @staticmethod
    def get_owner_user_id(api_key: str) -> int:
        url = urljoin(Testiny.__API_URL, "account/me")
        headers = {
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": api_key,
        }
        response = requests.request("GET", url, headers=headers, timeout=10)
        response.raise_for_status()

        response = response.json()
        if "error" in response.keys():
            raise ValueError("No user found associated with the given API key")
        return response["userId"]

    @staticmethod
    def create_test_case(file_path: str) -> int:
        """Creates a test case from a YAML file using the passed API key

        Args:
            file_path (str): path to the YAML file containing the test case

        Returns:
            int: The ID of the created test case
        """

        url = urljoin(Testiny.__API_URL, "testcase")

        data = Testiny.__read_test_case_file(file_path)

        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": get_configuration("api_key"),
        }

        payload = json.dumps(
            {
                "title": data["title"],
                "precondition_text": "\n".join(data["preconditions"]),
                "steps_text": "\n".join(data["steps"]),
                "expected_result_text": "\n".join(data["expected results"]),
                "project_id": data["project id"],
                "template": "TEXT",
                "owner_user_id": get_configuration("owner_user_id"),
            }
        )

        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=10
        )
        response.raise_for_status()

        return response.json()["id"]

    @staticmethod
    def update_test_case(
        file_path: str, test_case_id: int, *, _etag: str | None = None
    ) -> str:
        """Overwrites a test case from a YAML file using the passed API key

        Args:
            file_path (str): path to the YAML file containing the test case
            test_case_id (int): ID of the test case to update
            _etag (str, optional): ETag value for optimistic concurrency control. Defaults to None.

        Returns:
            str: The new _etag value returned by the API
        """
        url = urljoin(Testiny.__API_URL, f"testcase/{test_case_id}")
        data = Testiny.__read_test_case_file(file_path)

        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": get_configuration("api_key"),
        }

        payload = json.dumps(
            {
                "title": data["title"],
                "precondition_text": "\n".join(data["preconditions"]),
                "steps_text": "\n".join(data["steps"]),
                "expected_result_text": "\n".join(data["expected results"]),
                "project_id": data["project id"],
                "template": "TEXT",
                "owner_user_id": get_configuration("owner_user_id"),
                "_etag": _etag
                if _etag is not None
                else Testiny.__get_etag(test_case_id),
            }
        )

        response = requests.request(
            "PUT", url, headers=headers, data=payload, timeout=10
        )
        response.raise_for_status()

        return response.json()["_etag"]

    @staticmethod
    def __get_test_case_json(test_case_id: int) -> Any:
        """Reads a test case using the passed API key

        Args:
            test_case_id (int): ID of the test case to read

        Returns:
            Any: The test case object
        """
        url = urljoin(Testiny.__API_URL, f"testcase/{test_case_id}")
        headers = {
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": get_configuration("api_key"),
        }

        response = requests.request("GET", url, headers=headers, timeout=10)
        response.raise_for_status()

        return response.json()

    @staticmethod
    def upsert_test_case(file_path: str) -> Tuple[UpsertAction, int]:
        """Creates or updates a test case from a YAML file using the passed API key

        Args:
            file_path (str): path to the YAML file containing the test case

        Returns:
            Tuple[UpsertAction, int]: a tuple containing the action performed (create or update)
                and the test case ID
        """
        data = Testiny.__read_test_case_file(file_path)
        test_case = Testiny.__find_test_case_by_title(data["title"])

        if test_case is None:
            test_case_id = Testiny.create_test_case(file_path)
            return UpsertAction.CREATE, test_case_id
        else:
            test_case_id, etag = test_case
            Testiny.update_test_case(file_path, test_case_id, _etag=etag)
            return UpsertAction.UPDATE, test_case_id

    @staticmethod
    def read_test_case(test_case_id: int) -> str:
        """Reads a test case using the passed API key

        Args:
            test_case_id (int): ID of the test case to read

        Returns:
            str: The test case in a human-readable format, with Rich colors
        """
        test_case = Testiny.__get_test_case_json(test_case_id)

        NEW_LINE = "\n"
        return (
            f"[cyan]Title[/cyan]: {test_case['title']}\n"
            f"[cyan]Preconditions[/cyan]: \n{NEW_LINE.join(f'  - {line}' for line in test_case['precondition_text'].split(NEW_LINE))}\n"
            f"[cyan]Steps[/cyan]: \n{NEW_LINE.join(f'  - {line}' for line in test_case['steps_text'].split(NEW_LINE))}\n"
            f"[cyan]Expected Results[/cyan]: \n{NEW_LINE.join(f'  - {line}' for line in test_case['expected_result_text'].split(NEW_LINE))}\n"
            f"[cyan]Project ID[/cyan]: {test_case['project_id']}"
        )

    @staticmethod
    def get_project_id(project_name: str) -> int | None:
        """Gets the ID of a project by its name

        Args:
            project_name (str): The name of the project.

        Returns:
            int: The ID of the project if found or None if no project is found.
        """
        url = urljoin(Testiny.__API_URL, "project/find")
        payload = json.dumps({"filter": {"name": project_name}, "idOnly": True})
        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": get_configuration("api_key"),
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=10
        )
        response.raise_for_status()

        meta, data = response.json().values()

        if meta["count"] == 0:
            return None

        return data[0]["id"]

    @staticmethod
    def generate_test_case_template(test_title: str) -> str:
        """Generates a test case template with the given title.

        Args:
            test_title (str): The title of the test case.

        Returns:
            str: The generated test case template.
        """
        return (
            f"title: {test_title}\n"
            "preconditions:\n"
            "  - \n"
            "steps:\n"
            "  - \n"
            "expected results:\n"
            "  - \n"
        )
