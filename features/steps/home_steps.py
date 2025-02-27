from behave import given, when, then
from features.tests.utils.playwrightactions import PlaywrightActions
import os
import time
import json
from datetime import datetime

# Initialize screenshot counter and global variables
screenshot_counter = 1
registration_data = None

@given('I am on the local website')
def step_impl(context):
    global pa
    pa = PlaywrightActions(context.page)
    pa.navigate_to('http://localhost:5173/')
    print("I am on the local website")

@when('I load registration details from "{data_key}" in home.json')
def step_impl(context, data_key):
    global registration_data
    json_file_path = os.path.join('features', 'testdata', 'home.json')
    with open(json_file_path, 'r') as file:
        registration_data = json.load(file)[data_key]

@when('I enter the loaded registration details')
def step_impl(context):
    global registration_data
    # Wait for elements and fill the form with JSON data
    pa.wait_for_element('[data-testid="name-input"]')
    pa.wait_for_element('[data-testid="email-input"]')
    pa.wait_for_element('[data-testid="password-input"]')
    pa.fill_text('[data-testid="name-input"]', registration_data['name'])
    pa.fill_text('[data-testid="email-input"]', registration_data['email'])
    pa.fill_text('[data-testid="password-input"]', registration_data['password'])

@when('I enter the following registration details')
def step_impl(context):
    # Convert the data table to a dictionary
    data = {}
    for row in context.table:
        data[row['field']] = row['value']
    
    # Wait for elements and fill the form
    pa.wait_for_element('[data-testid="name-input"]')
    pa.wait_for_element('[data-testid="email-input"]')
    pa.wait_for_element('[data-testid="password-input"]')
    pa.fill_text('[data-testid="name-input"]', data['name'])
    pa.fill_text('[data-testid="email-input"]', data['email'])
    pa.fill_text('[data-testid="password-input"]', data['password'])

@then('I click the submit button')
def step_impl(context):
    global screenshot_counter
    pa.wait_for_element('[data-testid="submit-button"]')
    pa.click_element('[data-testid="submit-button"]')
    # Create timestamped folder for screenshots
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_folder = os.path.join('screenshots', f'User_Registration_Form_{timestamp}')
    os.makedirs(screenshot_folder, exist_ok=True)
    # Take a screenshot after form submission with sequential numbering
    screenshot_path = os.path.join(screenshot_folder, f'step_{screenshot_counter}.png')
    pa.take_screenshot(screenshot_path)
    screenshot_counter += 1
