from .Testiny import Testiny
from .TestManagementSystem import TestManagementSystem


TEST_MANAGEMENT_SYSTEMS = {
    "Testiny": Testiny,
}


class InvalidTestManagementSystemError(Exception):
    """
    Exception raised for invalid test management system.

    Attributes:
        system_name (str): The name of the invalid test management system.
        message (str): The error message.
    """

    def __init__(self, system_name: str, message: str = None):
        self.system_name = system_name
        if message is None:
            message = f"Test management system '{system_name}' is not supported."
        super().__init__(message)


@staticmethod
def get_test_management_system(system_name: str) -> TestManagementSystem:
    """
    Factory method to get an instance of the specified test management system.

    Args:
        system_name (str): The name of the test management system.

    Returns:
        TestManagementSystem: An instance of the specified test management system.

    Raises:
        InvalidTestManagementSystemError: If the specified test management system
            is not supported.
    """
    if system_name not in TEST_MANAGEMENT_SYSTEMS:
        raise InvalidTestManagementSystemError(system_name)
    return TEST_MANAGEMENT_SYSTEMS[system_name]()
