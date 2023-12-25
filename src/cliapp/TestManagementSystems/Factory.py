from TestManagementSystems.Testiny import Testiny
from TestManagementSystems.TestManagementSystem import TestManagementSystem


class Factory:
    __SYSTEMS = {
        "Testiny": Testiny,
    }

    @staticmethod
    def get_test_management_system(system_name: str) -> TestManagementSystem:
        if system_name not in Factory.__SYSTEMS:
            raise ValueError(
                f"Test management system `{system_name}` is not supported."
            )
        return Factory.__SYSTEMS[system_name]()
