from typing import Any, Dict, List, Tuple
from enum import Enum, auto
from urllib.parse import urljoin
import jsonschema
import requests
import yaml
import json
import os
from .utility import get_project_id, get_turbocase_configuration
from .enums import App, Project, UpsertAction


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
    def __read_test_case_file(file_path: str) -> Dict[str, Any]:
        """Reads a test case file in YAML format and validates it against a JSON schema

        Args:
            file_path (str): The path to the test case file.

        Returns:
            Dict[str, Any]: The content of the loaded test case.

        Raises:
            ValueError: If the file path does not refer to a valid YAML file.
        """
        if not file_path.endswith((".yaml", ".yml")):
            raise ValueError("File path does not refer to a valid YAML file")

        with open(file_path, "r", encoding="utf-8") as file:
            test_case_content = yaml.safe_load(file)

        with open(Testiny.__SCHEMA_FILE_PATH, "r", encoding="utf-8") as schema_file:
            schema = json.load(schema_file)

        jsonschema.validate(test_case_content, schema)

        return test_case_content

    @staticmethod
    def __find_test_case_by_title(
        title: str, projects_ids: List[int]
    ) -> List[Tuple[int, str]]:
        """Find a test case by its title.

        Args:
            title (str): The title of the test case.
            project (Project): The project to which the test case belongs.

        Returns:
            List[Tuple[int, str]]: A list of tuples containing the ID and ETag of the found test case.

        Raises:
            ValueError: If more than one test case is found with the given title.
        """
        url = urljoin(Testiny.__API_URL, "testcase/find")

        payload = json.dumps({"filter": {"title": title, "project_id": projects_ids}})
        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": get_turbocase_configuration("api_key"),
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=10
        )
        response.raise_for_status()

        test_cases = response.json()["data"]

        results = [(test_case["id"], test_case["_etag"]) for test_case in test_cases]

        return results

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
    def create_test_cases(
        test_title: str, app: App, project_path: str
    ) -> List[Tuple[int, Project]]:
        """
        Create test cases for each project in the given app using the provided file path and project path.

        Args:
            test_title (str): The title of the test case.
            app (App): The app object containing the projects.
            project_path (str): The path to the project.

        Returns:
            List[Tuple[int, Project]]: A list of tuples containing the test case ID and the corresponding project.
        """
        test_path = os.path.join(project_path, app.value.path, f"{test_title}.yaml")

        test_case_content = Testiny.__read_test_case_file(test_path)

        url = urljoin(Testiny.__API_URL, "testcase")

        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": get_turbocase_configuration("api_key"),
        }

        test_cases_ids = [
            (
                Testiny.__create_single_test_case(
                    get_project_id(project, project_path),
                    test_case_content,
                    headers,
                    url,
                ),
                project,
            )
            for project in app.value.projects
        ]

        return test_cases_ids

    @staticmethod
    def __create_single_test_case(
        project_id: int,
        test_case_content: Dict[str, Any],
        headers: Dict[str, Any],
        url: str,
    ) -> int:
        """
        Create a test case in a single Testiny project.

        Args:
            project (Project): The project to which the test case belongs.
            project_path (str): The path to the project folder.
            test_case_content (Dict[str, Any]): The test case content.
            headers (Dict[str, Any]): The request headers.
            url (str): The API URL for creating the test case.

        Returns:
            int: The ID of the created test case.
        """
        payload = json.dumps(
            {
                "title": test_case_content["title"],
                "precondition_text": "\n".join(test_case_content["preconditions"]),
                "steps_text": "\n".join(test_case_content["steps"]),
                "expected_result_text": "\n".join(
                    test_case_content["expected results"]
                ),
                "project_id": project_id,
                "template": "TEXT",
                "owner_user_id": get_turbocase_configuration("owner_user_id"),
            }
        )

        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=10
        )
        response.raise_for_status()

        return response.json()["id"]

    @staticmethod
    def update_test_cases(
        test_title: str, app: App, project_path: str
    ) -> List[Tuple[int, Project]]:
        """
        Update test cases for each project in the given app using the provided file path and project path.

        Args:
            test_title (str): The title of the test case.
            app (App): The app object containing the projects.
            project_path (str): The path to the project.

        Returns:
            List[Tuple[int, Project]]: A list of tuples containing the test case ID and the corresponding project.
        """
        test_path = os.path.join(project_path, app.value.path, f"{test_title}.yaml")

        test_case_content = Testiny.__read_test_case_file(test_path)

        projects_ids = [
            get_project_id(project, project_path) for project in app.value.projects
        ]

        found_test_cases = Testiny.__find_test_case_by_title(test_title, projects_ids)

        if not found_test_cases:
            raise ValueError(
                "No test case found with the given title. "
                "Please use the [yellow]`create`[/yellow] command."
            )

        test_cases_ids, etags = list(zip(*found_test_cases))

        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": get_turbocase_configuration("api_key"),
        }

        for project_id, test_case_id, etag in zip(projects_ids, test_cases_ids, etags):
            Testiny.__update_single_test_case(
                project_id, test_case_content, headers, test_case_id, etag
            )

        return list(zip(test_cases_ids, app.value.projects))

    @staticmethod
    def __update_single_test_case(
        project_id: int,
        test_case_content: Dict[str, Any],
        headers: Dict[str, Any],
        test_case_id: int,
        etag: str,
    ) -> int:
        """
        Update a test case in a single Testiny project.

        Args:
            project_id (int): The ID of the project.
            test_case_content (Dict[str, Any]): The content of the test case.
            headers (Dict[str, Any]): The headers for the API request.
            test_case_id (int): The ID of the test case to be updated.
            etag (str): The ETag value for optimistic concurrency control.

        Returns:
            int: The ID of the updated test case.
        """
        url = urljoin(Testiny.__API_URL, f"testcase/{test_case_id}")

        payload = json.dumps(
            {
                "title": test_case_content["title"],
                "precondition_text": "\n".join(test_case_content["preconditions"]),
                "steps_text": "\n".join(test_case_content["steps"]),
                "expected_result_text": "\n".join(
                    test_case_content["expected results"]
                ),
                "project_id": project_id,
                "template": "TEXT",
                "owner_user_id": get_turbocase_configuration("owner_user_id"),
                "_etag": etag,
            }
        )

        response = requests.request(
            "PUT", url, headers=headers, data=payload, timeout=10
        )
        response.raise_for_status()

        return response.json()["id"]

    @staticmethod
    def __get_test_case_json(test_case_id: int) -> Dict[str, Any]:
        """Reads a test case using the passed API key

        Args:
            test_case_id (int): ID of the test case to read

        Returns:
            Dict[str, Any]: The content of the test case
        """
        url = urljoin(Testiny.__API_URL, f"testcase/{test_case_id}")
        headers = {
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": get_turbocase_configuration("api_key"),
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
            "X-Api-Key": get_turbocase_configuration("api_key"),
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
