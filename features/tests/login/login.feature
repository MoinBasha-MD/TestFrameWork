Feature: Login Functionality
    As a user
    I want to login to the application
    So that I can access my account

    Scenario: Successful login with valid credentials
        Given I am on the login page
        When I enter valid username and password
        And I click the login button
        Then I should be logged in successfully