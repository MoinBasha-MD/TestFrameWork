from behave import given, when, then
import json
import os

@given('I load {test_data_file} and {data_set}')
def load_test_data(context, test_data_file, data_set):
    # Remove angle brackets if present
    test_data_file = test_data_file.strip('<>')
    data_set = data_set.strip('<>')
    
    # Load the test data file
    test_data_path = os.path.join('features', 'tests', 'testdata', test_data_file)
    context.test_data = require(test_data_path)
    
    # Verify the dataset exists
    if context.test_data['dataSet'] != data_set:
        raise ValueError(f"Dataset {data_set} not found in {test_data_file}")

@given('I navigate to CNS logon screen as per the {environment}')
def navigate_to_cns_logon(context, environment):
    environment = environment.strip('<>')
    # Add navigation logic here
    context.environment = environment

@when('I click on Individual Pension {business_link} link on CNS')
def click_individual_pension(context, business_link):
    business_link = business_link.strip('<>')
    # Add click logic here
    context.business_link = business_link

@when('I enter branch code in Sales Point Details page for EB Java journey')
def enter_branch_code(context):
    # Use branch code from test data
    branch_code = context.test_data.get('branchCode')
    # Add implementation to enter branch code

@when('I click next on Adviser Charges page for EB Designation Authorize Java journey')
def click_next_adviser_charges(context):
    # Add implementation to handle adviser charges page
    pass

@when('I click next on Designate Funds page for EB Designation Authorize Java journey')
def click_next_designate_funds(context):
    # Add implementation to handle designate funds page
    pass

@when('I click next on Income & Tax Free Cash Details page for EB Designation Authorize Java journey')
def click_next_income_tax(context):
    # Add implementation to handle income and tax details page
    pass

@when('I select LTA certified on Authorization Confirmation page for EB Designation Authorize Java journey')
def select_lta_certified(context):
    # Use LTA certified setting from test data
    lta_certified = context.test_data.get('incomeTaxDetails', {}).get('ltaCertified')
    # Add implementation to select LTA certified

@when('I click next on Authorization Confirmation page for EB Designation Authorize Java journey')
def click_next_authorization(context):
    # Add implementation to handle authorization confirmation
    pass

@when('I click finish on Authorization Request Submit page for EB Designation Authorize Java journey')
def click_finish_authorization(context):
    # Add implementation to handle authorization submit
    pass