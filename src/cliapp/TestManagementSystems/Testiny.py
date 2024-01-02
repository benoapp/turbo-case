from TestManagementSystems.TestManagementSystem import TestManagementSystem
import requests
import yaml
import json
import jsonschema
import os
from overrides import override


class Testiny(TestManagementSystem):
    __CONTENT_TYPE = "application/json"
    __SCHEMA_FILE_PATH = os.path.join(
        os.path.dirname(__file__), "testiny_schema.json"
    )  # TODO: write this in a better (safer) way

    @staticmethod
    def __get_owner_id(api_key: str) -> int:
        url = "https://app.testiny.io/api/v1/account/me"
        headers = {
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": api_key,
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        response = response.json()
        if "error" in response.keys():
            raise ValueError("No user found associated with the given API key")
        return response["userId"]

    @staticmethod
    def __read_test_case_schema(file_path: str):
        if not file_path.endswith((".yaml", ".yml")):
            raise ValueError("File path does not refer to a valid YAML file")

        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        with open(Testiny.__SCHEMA_FILE_PATH, "r") as schema_file:
            schema = json.load(schema_file)

        jsonschema.validate(data, schema)

        return data

    @staticmethod
    @override
    def create_test_case(file_path: str, api_key: str):
        url = "https://app.testiny.io/api/v1/testcase"

        data = Testiny.__read_test_case_schema(file_path)

        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": api_key,
        }

        payload = json.dumps(
            {
                "title": data["title"],
                "precondition_text": "\n".join(data["preconditions"]),
                "steps_text": "\n".join(data["steps"]),
                "expected_result_text": "\n".join(data["expected results"]),
                "project_id": data["project id"],
                "template": "TEXT",
                "owner_user_id": Testiny.__get_owner_id(api_key),
            }
        )

        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()

    @staticmethod
    @override
    def update_test_case(file_path: str, api_key: str, test_case_id: int) -> None:
        url = f"https://app.testiny.io/api/v1/testcase/{test_case_id}"

        data = Testiny.__read_test_case_schema(file_path)

        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": api_key,
        }

        payload = json.dumps(
            {
                "title": data["title"],
                "precondition_text": "\n".join(data["preconditions"]),
                "steps_text": "\n".join(data["steps"]),
                "expected_result_text": "\n".join(data["expected results"]),
                "project_id": data["project id"],
                "template": "TEXT",
                "owner_user_id": Testiny.__get_owner_id(api_key),
            }
        )

        response = requests.request("PUT", url, headers=headers, data=payload)
        response.raise_for_status()

    @staticmethod
    def read_test_case(api_key: str, test_case_id: int):
        url = f"https://app.testiny.io/api/v1/testcase/{test_case_id}"

        headers = {
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": api_key,
        }

        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()

        return response.json()
