from setuptools import setup, find_packages
from turbocase.__init__ import __version__

with open("requirements.txt", "r", encoding="UTF-8") as file:
    requirements = [line.strip() for line in file.readlines()]

with open("README.md", "r", encoding="UTF-8") as file:
    README = file.read()


setup(
    name="turbocase",
    version=__version__,
    python_requires=">=3.6",
    url="https://github.com/benoapp/turbo-case",
    author="Ahmad Alsaleh",
    author_email="ahmed.asaleh2@gmail.com",
    description="A CLI App to enable manual-test-case-as-code",
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    package_data={"TestManagementSystems": ["Testiny_schema.json"]},
    entry_points={
        "console_scripts": [
            "turbocase = turbocase.main:main",
        ]
    },
)
