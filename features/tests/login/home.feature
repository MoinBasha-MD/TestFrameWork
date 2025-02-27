Feature: User Registration Form

    Scenario Outline: Open local website and fill and submit the form using JSON data
        Given I am on the local website
        When I load registration details from "<data_key>" in registration_data.json
        And I enter the following registration details
            | entertext | locator           | action |
            | name      | #name             | Fill   |
            | email     | #email            | Fill   |
            | password  | #password         | Fill   |
          
        Then I click element to submit the form

    Examples:
        | data_key     |
        | USER_REG_01  |
        # | USER_REG_02  |
    