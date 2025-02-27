from behave import given, when, then
from playwright.sync_api import expect
import json

def load_test_data(data_file, key):
    with open(data_file, 'r') as f:
        data = json.load(f)
    return data.get(key)

@when('I load registration details from "{data_key}" in registration_data.json')
def step_impl(context, data_key):
    context.registration_data = load_test_data('features/testdata/registration_data.json', data_key)

@when('I enter the following registration details')
def step_impl(context):
    for row in context.table:
        data_key = row['entertext'].lower()
        locator = row['locator']
        action = row['action'].lower()
        
        # Get the value from the loaded data
        value = context.registration_data.get(data_key)
        
        if action == 'fill':
            context.page.fill(locator, value)
        elif action == 'click':
            context.page.click(locator)
        elif action == 'select':
            context.page.select_option(locator, value)

@then('I click element with locator "{locator}" to submit the form')
def step_impl(context, locator):
    # Wait for element to be visible and enabled before clicking
    context.page.wait_for_selector(locator, state='visible', timeout=45000)
    element = context.page.locator(locator)
    expect(element).to_be_enabled(timeout=45000)
    element.click()