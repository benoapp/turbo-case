from TestManagementSystems.TestManagementSystem import TestManagementSystem
import requests
import yaml
import json
import jsonschema
import os


class Testiny(TestManagementSystem):
    __CONTENT_TYPE = "application/json"
    __SCHEMA_FILE_PATH = os.path.join(os.path.dirname(__file__), "testiny_schema.json")

    @staticmethod
    def __get_owner_id(api_key: str) -> int:
        url = "https://app.testiny.io/api/v1/account/me"
        headers = {
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": api_key,
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        user_id = response.json()["userId"]
        if user_id == "No user context":
            raise ValueError("No user found associated with the API key")
        return user_id

    @staticmethod
    def __read_test_case(file_path: str):
        if not file_path.endswith((".yaml", ".yml")):
            raise ValueError("File path does not refer to a valid YAML file")

        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        with open(Testiny.__SCHEMA_FILE_PATH, "r") as schema_file:
            schema = json.load(schema_file)

        jsonschema.validate(data, schema)

        return data

    @staticmethod
    def create_test_case(file_path: str, api_key: str):
        data = Testiny.__read_test_case(file_path)

        url = "https://app.testiny.io/api/v1/testcase"

        headers = {
            "Content-Type": Testiny.__CONTENT_TYPE,
            "Accept": Testiny.__CONTENT_TYPE,
            "X-Api-Key": api_key,
        }

        payload = {
            "title": data["title"],
            "precondition_text": "\n".join(data["preconditions"]),
            "steps_text": "\n".join(data["steps"]),
            "expected_result_text": "\n".join(data["expected results"]),
            "project_id": data["project id"],
            "template": "TEXT",
            "owner_user_id": Testiny.__get_owner_id(api_key),
        }

        payload = json.dumps(payload)

        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
