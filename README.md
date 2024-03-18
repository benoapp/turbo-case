# Turbo-Case

![turbocase-preview](assets/turbocase-preview.svg)

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)


Enable manual-test-case-as-code for [Testiny](https://www.testiny.io/).

## Table of contents
- [Turbo-Case](#turbo-case)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
  - [Setup](#setup)
  - [Usage](#usage)
    - [Generating a test file](#generating-a-test-file)
    - [Edit the YAML test file](#edit-the-yaml-test-file)
    - [Uploading test cases to Testiny](#uploading-test-cases-to-testiny)
    - [Updating a test case](#updating-a-test-case)
    - [Reading a test case](#reading-a-test-case)
    - [Using the `upsert` command](#using-the-upsert-command)
    - [Extra Information](#extra-information)
  - [Contribution Guide](#contribution-guide)
- [References](#references)


## Installation

Install from PyPI (recommended):
```shell
TODO (use pipx not pip)
```

Or, from GitHub (development version):
```shell
pipx install git+https://github.com/benoapp/turbo-case.git
```


You can generate an Testiny API key by the following the instructions [here](https://app.testiny.io/settings/apikeys).

## Setup

Turbocase is an opinionated tool that assumes you have an App available for all platforms (web, ios, and Android).

1. Use `turbocase init` to initialize a test management project in the current directory.

This command will automatically create the following folder structure:

```shell
.
├── .turbocase/project.toml
└── app
    ├── web
    └── mobile
        ├── android
        └── ios
```

2. Configure your test management tool

Current Supported Systems
- Testiny 

A guide to how to add support a new test management system soon.

Next, configure `turbocase` by running the following:
```shell
turbocase config --tool Testiny
```

Turbo case will guide you through config steps. It usually includes:
- entering the api key
- mapping each project with the test management tool


3. You can import test cases from a Test Management System

Use the command `turbocase import`

## Usage

### Generating a test file

#### Generate a Test from a Feature

TurboCase can generate test files from requirements files. Currently it supports `.feature` files.

```shell
turbocase generate testcase --file new.feature 
```

> Note that `@app:<app>` must be added. Also, you may add `@platform:<platform>` to specify which platform.

#### Generate a Standalone Test

TurboCase can generate a test file from CLI. Curretnly, it supports the `title` field. Other fields will need to be filled in the file.

```shell
turbocase generate testcase [app|web|mobile|android|ios] "Title of Test Case"
```

#### Import a Testcase

Turbocase can import testcases from your Test Management platform.

```shell
turbocase import 123
```

### Edit the YAML test file

The YAML file should contain `title`, `preconditions`, `steps`, and `expected results` (all case sensitive), as in the following example:

```yaml
title: Payment Gateway Works
preconditions: |
    # new user
    - User logged in
    - Cart is not empty
steps: |
    # user checks out a deal
    - Click on checkout 
    - Fill credit card information
    - Click on pay
expected results: |
    # payment is successfull
    - Success
```

### Uploading test cases to Testiny

Test cases can be created and uploaded to [Testiny](https://www.testiny.io/) using the following:

* Single file

```shell
turbocase create test_case.yaml
```

* Multiple files

```shell
turbocase create test_one.yaml test_two.yaml

# OR, using a folder
turbocase create test_cases/*
```

### Updating a test case

To update a specific test case, run the following:
```shell
turbocase update --id 192 new_test_case.yaml
```

### Reading a test case

To read a test case, run the following
```shell
turbocase read --id 192
```

### Using the `upsert` command
To create or update an existing test case, use the `upsert` command. This command will try to update an existing test case with the same title instead of creating a new one. If no such test case exists, a new one will be created automatically.

```shell
turbocase upsert test_case.yaml
```

### Extra Information
For more information, run `turbocase --help` or `turbocase <command> --help`.

## Contribution Guide

If you have suggestions, please create a [GitHub Issue](https://github.com/benoapp/turbo-case/issues/new/choose).

# References

- [Testiny API Documentation](https://www.testiny.io/docs/rest-api/testiny-api/)
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
