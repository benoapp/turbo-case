from abc import ABC, abstractmethod
from typing import Any
from typing import Tuple
from enum import Enum
from overrides import EnforceOverrides


class UpsertAction(Enum):
    """
    Enum representing the action to perform during an upsert operation.

    Possible values:
    - UPDATE: Indicates that the existing item was updated.
    - CREATE: Indicates that a new item was created.
    """

    UPDATE = "update"
    CREATE = "create"


class TestManagementSystem(ABC, EnforceOverrides):
    """Abstract base class for test management systems"""

    @staticmethod
    @abstractmethod
    def create_test_case(file_path: str, api_key: str) -> int:
        """Creates a test case from a YAML file using the passed API key

        Args:
            file_path (str): path to the YAML file containing the test case
            api_key (str): API key to use for creating the test case

        Returns:
            int: The ID of the created test case
        """

    @staticmethod
    @abstractmethod
    def update_test_case(
        file_path: str, api_key: str, test_case_id: int, *, _etag: str = None
    ) -> str:
        """Overwrites a test case from a YAML file using the passed API key

        Args:
            file_path (str): path to the YAML file containing the test case
            api_key (str): API key to use for updating the test case
            test_case_id (int): ID of the test case to update
            _etag (str, optional): ETag value for optimistic concurrency control. Defaults to None.

        Returns:
            str: The new _etag value if it is returned by the API
        """

    @staticmethod
    @abstractmethod
    def read_test_case(api_key: str, test_case_id: int) -> Any:
        """Reads a test case using the passed API key

        Args:
            api_key (str): API key to use for reading the test case
            test_case_id (int): ID of the test case to read

        Returns:
            Any: The test case object
        """

    @staticmethod
    @abstractmethod
    def upsert_test_case(file_path: str, api_key: str) -> Tuple[UpsertAction, int]:
        """Creates or updates a test case from a YAML file using the passed API key

        Args:
            file_path (str): path to the YAML file containing the test case
            api_key (str): API key to use for creating/updating the test case

        Returns:
            Tuple[UpsertAction, int]: a tuple containing the action performed (create or update)
                and the test case ID
        """
