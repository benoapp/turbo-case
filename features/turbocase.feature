Feature: TurboCase

    Scenario: Bundle a test case

        Given a manual test file
        When I run "bundle" command
        And specify "--testmanagement Testiny"
        Then I should get a csv with my test cases

