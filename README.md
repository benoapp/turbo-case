# TurboCase

A CLI App to enable manual-test-case-as-code

## How to use

1. Create a test file:
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

2. sync with Testiny
```shell
# single file
turbocase export --testmanagement Testiny src/partial.feature.yaml
# multiple files
turbocase export --testmanagement Testiny src/*
```
## Contribution Guide

Follow Git commits that comply with [Conventional Commits](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)

## References:
- [Testiny CLI](https://www.testiny.io/docs/automation/reference/)
- [Testiny API](https://www.testiny.io/docs/rest-api/testiny-api/)
- [Python Click](https://click.palletsprojects.com/en/8.1.x/)
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
