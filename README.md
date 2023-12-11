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

4. BDD
```gherkin
Feature: TurboCase

    Scenario: Bundle a test case

        Given a manual test file
        When I run "bundle" command
        And specify "--testmanagement Testiny"
        Then I should get a csv with my test cases
```

# References:
- [Testiny CLI](https://www.testiny.io/docs/automation/reference/)
- [Testiny API](https://www.testiny.io/docs/rest-api/testiny-api/)
- [Python Click](https://click.palletsprojects.com/en/8.1.x/)

