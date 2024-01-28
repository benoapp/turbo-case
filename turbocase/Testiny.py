from typing import Any, Dict, List, Tuple
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
    def __create_test_case_in_single_project(
        test_title: str,
        project_id: int,
        test_case_content: Dict[str, Any],
        headers: Dict[str, Any],
    ) -> int:
        """
        Create a test case in a single Testiny project.

        Args:
            test_title (str): The title of the test case.
            project_id (int): The ID of the project.
            test_case_content (Dict[str, Any]): The content of the test case.
            headers (Dict[str, Any]): The headers for the API request.

        Returns:
            int: The ID of the created test case.
        """
        url = urljoin(Testiny.__API_URL, "testcase")

        payload = json.dumps(
            {
                "title": test_title,
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
    def __update_test_case_in_single_project(
        test_title: str,
        project_id: int,
        test_case_content: Dict[str, Any],
        headers: Dict[str, Any],
        test_case_id: int,
        etag: str,
    ) -> int:
        """
        Update a test case in a single Testiny project.

        Args:
            test_title (str): The title of the test case.
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
                "title": test_title,
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
    def upsert_test_case(
        test_title: str, app: App, project_path: str
    ) -> Tuple[UpsertAction, List[Tuple[int, Project]]]:
        """Creates or updates a test case from a YAML file using the passed API key

        Args:
            file_path (str): path to the YAML file containing the test case
            app (str): The name of the app to which the test case belongs
            project_path (str): The path to the project folder

        Returns:
            Tuple[UpsertAction, List[Tuple[int, Project]]]: A tuple containing the action performed
                and a list of tuples containing the test case ID and project name of the created/updated test case
        """
        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": get_turbocase_configuration("api_key"),
        }

        test_path = os.path.join(project_path, app.value.path, f"{test_title}.yaml")
        test_case_content = Testiny.__read_test_case_file(test_path)

        projects_ids = [
            get_project_id(project, project_path) for project in app.value.projects
        ]

        found_test_cases = Testiny.__find_test_case_by_title(test_title, projects_ids)

        if found_test_cases:
            test_cases_ids, etags = list(zip(*found_test_cases))
            for project_id, test_case_id, etag in zip(
                projects_ids, test_cases_ids, etags
            ):
                Testiny.__update_test_case_in_single_project(
                    test_title,
                    project_id,
                    test_case_content,
                    headers,
                    test_case_id,
                    etag,
                )
            upsert_operation = UpsertAction.UPDATE
        else:
            test_cases_ids = []
            for project_id in projects_ids:
                test_case_id = Testiny.__create_test_case_in_single_project(
                    test_title,
                    project_id,
                    test_case_content,
                    headers,
                )
                test_cases_ids.append(test_case_id)
            upsert_operation = UpsertAction.CREATE

        return upsert_operation, list(zip(test_cases_ids, app.value.projects))

    @staticmethod
    def read_test_case(test_case_id: int) -> str:
        """Reads a test case using the passed API key

        Args:
            test_case_id (int): ID of the test case to read

        Returns:
            str: The test case in a human-readable format, with Rich colors
        """
        test_case = Testiny.__get_test_case_json(test_case_id)

        format_list = lambda text: "\n".join(f"  - {line}" for line in text.split("\n"))

        return (
            f"[cyan]Preconditions[/cyan]:\n{format_list(test_case['precondition_text'])}\n"
            f"[cyan]Steps[/cyan]:\n{format_list(test_case['steps_text']) }\n"
            f"[cyan]Expected Results[/cyan]:\n{format_list(test_case['expected_result_text'])}\n"
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
    def generate_test_case_template() -> str:
        """Generates a test case template with the given title.

        Returns:
            str: The generated test case template.
        """
        return (
            "preconditions:\n"
            "  - \n"
            "steps:\n"
            "  - \n"
            "expected results:\n"
            "  - \n"
        )
