Feature: partial payments
  Scenario: Even
    When checkout 10
    Then pay 5 now
    And pay 5 later
