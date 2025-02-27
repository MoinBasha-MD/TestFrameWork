Feature: User Registration Form

    Scenario Outline: Open local website and fill and submit the form using JSON data
        Given I am on the local website
        When I load registration details from "<data_key>" in home.json
        And I enter the loaded registration details
        Then I click the submit button

    Examples:
        | data_key     |
        | registration |
    