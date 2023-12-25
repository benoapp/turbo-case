# TurboCase

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

A CLI App to enable manual-test-case-as-code

## Supported Test Management Systems:
Currently, the following test management systems are supported:
1. [Testiny](https://www.testiny.io/)

## How to use

## Creating a new test case

1. Create a test file using YAML:

```yaml
title: string
preconditions:
  - string
steps:
  - string
expected results:
  - string
project id: 2
```

2. Submit test case to the test management system

```shell
turbocase create test_one.yaml test_two.yaml --system <NAME> --api-key <KEY> 
```

## Contribution Guide

Follow Git commits that comply with [Conventional Commits](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)

# References:

- [Testiny CLI](https://www.testiny.io/docs/automation/reference/)
- [Testiny API](https://www.testiny.io/docs/rest-api/testiny-api/)
- [Python argparse](https://docs.python.org/3/library/argparse.html)
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
