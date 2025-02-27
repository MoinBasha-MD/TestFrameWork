from playwright.sync_api import sync_playwright
from features.tests.utils.screenshot_manager import ScreenshotManager

def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False)
    context.screenshot_manager = ScreenshotManager()

def before_scenario(context, scenario):
    context.browser_context = context.browser.new_context()
    context.page = context.browser_context.new_page()

def after_scenario(context, scenario):
    context.browser_context.close()

def after_step(context, step):
    # Take screenshot after each step
    if hasattr(context, 'page'):
        context.screenshot_manager.take_step_screenshot(context, step.name)

def after_step_failed(context, step):
    # Take screenshot when a step fails
    if hasattr(context, 'page'):
        context.screenshot_manager.take_error_screenshot(context, step.name)

def after_all(context):
    context.browser.close()
    context.playwright.stop()