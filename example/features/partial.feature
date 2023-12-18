Feature: partial payments
  Scenario: Even
    When checkout 10
    Then pay 5 now
    And pay 5 later

  Scenario: Odd
    When Checkout 11
    Then Pay 6 now
    And Pay 5 later
