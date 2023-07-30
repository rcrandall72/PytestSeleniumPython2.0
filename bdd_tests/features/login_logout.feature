Feature: User Login and Logout
    As a user
    I want to log in and out of the application
    So that I can access my account and ensure security

Scenario: Login and Logout
    Given the user is on the login page
    When the user enters a valid username/password and logs in
    Then the user should be on the main homepage
    When the user logs out
    Then the user should be on the login page

Scenario: Failed Login - Incorrect Password
    Given the user is on the login page
    When the user enters invalid credentials and clicks the login button
    Then an error message should be displayed