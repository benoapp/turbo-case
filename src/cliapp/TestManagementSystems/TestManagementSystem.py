from abc import ABC, abstractmethod
from typing import Any
from overrides import EnforceOverrides


class TestManagementSystem(ABC, EnforceOverrides):
    @staticmethod
    @abstractmethod
    def create_test_case(file_path: str, api_key: str):
        """Creates a test case from a YAML file using the passed API key

        Args:
            file_path (str): path to the YAML file containing the test case
            api_key (str): API key to use for creating the test case
        """
        pass

    @staticmethod
    @abstractmethod
    def update_test_case(file_path: str, api_key: str, test_case_id: int):
        """Overwrites a test case from a YAML file using the passed API key

        Args:
            file_path (str): path to the YAML file containing the test case
            api_key (str): API key to use for updating the test case
        """
        pass

    @staticmethod
    @abstractmethod
    def read_test_case(api_key: str, test_case_id: int) -> Any:
        """Reads a test case using the passed API key

        Args:
            api_key (str): API key to use for reading the test case
            test_case_id (int): ID of the test case to read
        """
        pass
