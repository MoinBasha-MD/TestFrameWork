from behave import given, when, then
from playwright.sync_api import expect

@given('I am on the login page')
def step_impl(context):
    context.page.goto('http://your-application-url/login')

@when('I enter valid username and password')
def step_impl(context):
    context.page.fill('input[name="username"]', 'test_user')
    context.page.fill('input[name="password"]', 'test_password')

@when('I click the login button')
def step_impl(context):
    context.page.click('button[type="submit"]')

@then('I should be logged in successfully')
def step_impl(context):
    # Add appropriate assertion based on your application
    expect(context.page).to_have_url('http://your-application-url/dashboard')
    expect(context.page.locator('.user-profile')).to_be_visible()