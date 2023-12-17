# TurboCase
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)

A CLI App to enable manual-test-case-as-code

## How to use

1. Create a test file using YAML:

```yaml
#
title: string
precondition:
  - string
steps:
  - string
expect:
  - string
```

2. Sync with Testiny

```shell
# single file
turbocase export --test-management Testiny src/partial.feature.yaml

# multiple files
turbocase export --test-management Testiny src/*
```

## Contribution Guide

Follow Git commits that comply with [Conventional Commits](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)

# References:

- [Testiny CLI](https://www.testiny.io/docs/automation/reference/)
- [Testiny API](https://www.testiny.io/docs/rest-api/testiny-api/)
- [Python argparse](https://docs.python.org/3/library/argparse.html)
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
