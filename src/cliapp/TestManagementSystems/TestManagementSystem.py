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
