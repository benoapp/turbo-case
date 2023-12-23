import yaml
import json
import requests
from abc import ABC, abstractmethod


class TestManagementSystem(ABC):
    @staticmethod
    @abstractmethod
    def create_test_case(file_path: str, api_key: str):
        """Creates a test case from a YAML file using the passed API key

        Args:
            file_path (str): path to the YAML file containing the test case
            api_key (str): API key to use for creating the test case
        """
        pass


class Testiny(TestManagementSystem):
    __CONTENT_TYPE = "application/json"

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
            raise ValueError("No user context found associated with the API key.")
        return user_id

    @staticmethod
    def create_test_case(file_path: str, api_key: str):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

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


def get_test_system(system_name: str) -> TestManagementSystem:
    if system_name == "Testiny":
        return Testiny()
    else:
        raise ValueError(f"Test system '{system_name}' is not supported.")
