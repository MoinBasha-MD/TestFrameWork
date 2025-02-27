from behave import given, when, then
from features.tests.utils.playwrightactions import PlaywrightActions
import os
import time
import json
from datetime import datetime

# Initialize screenshot counter and global variables
screenshot_counter = 1

@given('I am on the local website')
def step_impl(context):
    global pa
    pa = PlaywrightActions(context.page)
    pa.navigate_to('http://localhost:5173/')
    print('I am on the local website. Ammu')

@when('I enter the loaded registration details')
def step_impl(context):
    # Wait for elements and fill the form with JSON data
    pa.wait_for_element('[data-testid="name-input"]')
    # Additional form handling logic can be added here
@Then ('I click element to submit the form')
def submit_form(context):
    # Click the submit button
    pa.click_element('[data-testid="submit-button"]')
    print("I click element to submit the form")