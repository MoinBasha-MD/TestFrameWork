from playwright.sync_api import Page, expect, TimeoutError
from typing import Dict, List, Optional, Union
import json
import os

class ElementNotFoundError(Exception):
    """Raised when an element cannot be found on the page"""
    pass

class ElementNotVisibleError(Exception):
    """Raised when an element is found but not visible"""
    pass

class ActionTimeoutError(Exception):
    """Raised when an action times out"""
    pass

class PlaywrightActions:
    def __init__(self, page: Page):
        self.page = page
        self.locator_repository = {}
        self._load_locator_repository()

    def _load_locator_repository(self):
        """Load locators from JSON files in the locators directory"""
        locators_dir = os.path.join(os.path.dirname(__file__), 'locators')
        if os.path.exists(locators_dir):
            for file in os.listdir(locators_dir):
                if file.endswith('.json'):
                    file_path = os.path.join(locators_dir, file)
                    with open(file_path, 'r') as f:
                        self.locator_repository.update(json.load(f))

    def _resolve_locator(self, selector: str) -> str:
        """Resolve locator from repository if it starts with '@', otherwise return as is"""
        if selector.startswith('@'):
            key = selector[1:]
            if key not in self.locator_repository:
                raise ValueError(f"Locator '{key}' not found in repository")
            return self.locator_repository[key]
        return selector

    def navigate_to(self, url: str):
        """Navigate to the specified URL"""
        try:
            self.page.goto(url)
        except TimeoutError:
            raise ActionTimeoutError(f"Timeout while navigating to {url}")

    def click_element(self, selector: str):
        """Click on an element identified by selector"""
        try:
            resolved_selector = self._resolve_locator(selector)
            element = self.page.locator(resolved_selector)
            if not element.is_visible():
                raise ElementNotVisibleError(f"Element with selector '{resolved_selector}' is not visible")
            element.click()
        except TimeoutError:
            raise ElementNotFoundError(f"Element with selector '{resolved_selector}' not found")

    def fill_text(self, selector: str, text: str):
        """Fill text in an input field"""
        try:
            resolved_selector = self._resolve_locator(selector)
            element = self.page.locator(resolved_selector)
            if not element.is_visible():
                raise ElementNotVisibleError(f"Input field with selector '{resolved_selector}' is not visible")
            element.fill(text)
        except TimeoutError:
            raise ElementNotFoundError(f"Input field with selector '{resolved_selector}' not found")

    def get_text(self, selector: str) -> str:
        """Get text content of an element"""
        try:
            resolved_selector = self._resolve_locator(selector)
            element = self.page.locator(resolved_selector)
            if not element.is_visible():
                raise ElementNotVisibleError(f"Element with selector '{resolved_selector}' is not visible")
            return element.text_content()
        except TimeoutError:
            raise ElementNotFoundError(f"Element with selector '{resolved_selector}' not found")

    def is_element_visible(self, selector: str) -> bool:
        """Check if an element is visible"""
        try:
            resolved_selector = self._resolve_locator(selector)
            return self.page.locator(resolved_selector).is_visible()
        except TimeoutError:
            return False

    def wait_for_element(self, selector: str):
        """Wait for an element to be visible"""
        try:
            resolved_selector = self._resolve_locator(selector)
            self.page.wait_for_selector(resolved_selector)
        except TimeoutError:
            raise ElementNotFoundError(f"Timeout waiting for element with selector '{resolved_selector}'")

    def expect_url(self, url: str):
        """Expect current URL to match the specified URL"""
        try:
            expect(self.page).to_have_url(url)
        except TimeoutError:
            raise ActionTimeoutError(f"URL did not match '{url}' within timeout period")

    def expect_element_visible(self, selector: str):
        """Expect an element to be visible"""
        try:
            expect(self.page.locator(selector)).to_be_visible()
        except TimeoutError:
            raise ElementNotVisibleError(f"Element with selector '{selector}' did not become visible")

    def select_option(self, selector: str, value: str):
        """Select an option from a dropdown"""
        try:
            element = self.page.locator(selector)
            if not element.is_visible():
                raise ElementNotVisibleError(f"Dropdown with selector '{selector}' is not visible")
            element.select_option(value)
        except TimeoutError:
            raise ElementNotFoundError(f"Dropdown with selector '{selector}' not found")

    def type_text(self, selector: str, text: str, delay: int = 0):
        """Type text with optional delay between keystrokes"""
        try:
            element = self.page.locator(selector)
            if not element.is_visible():
                raise ElementNotVisibleError(f"Input field with selector '{selector}' is not visible")
            element.type(text, delay=delay)
        except TimeoutError:
            raise ElementNotFoundError(f"Input field with selector '{selector}' not found")

    def hover_element(self, selector: str):
        """Hover over an element"""
        try:
            element = self.page.locator(selector)
            if not element.is_visible():
                raise ElementNotVisibleError(f"Element with selector '{selector}' is not visible")
            element.hover()
        except TimeoutError:
            raise ElementNotFoundError(f"Element with selector '{selector}' not found")

    def get_element_attribute(self, selector: str, attribute: str) -> str:
        """Get attribute value of an element"""
        try:
            element = self.page.locator(selector)
            if not element.is_visible():
                raise ElementNotVisibleError(f"Element with selector '{selector}' is not visible")
            return element.get_attribute(attribute)
        except TimeoutError:
            raise ElementNotFoundError(f"Element with selector '{selector}' not found")

    def take_screenshot(self, path: str, full_page: bool = True):
        """Take a screenshot of the current page
        Args:
            path (str): Path where to save the screenshot
            full_page (bool, optional): Whether to take a full page screenshot. Defaults to True.
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.page.screenshot(path=path, full_page=full_page)
        except Exception as e:
            raise ActionTimeoutError(f"Failed to take screenshot: {str(e)}")

    def handle_iframe(self, frame_selector: str) -> Page:
        """Switch to an iframe context"""
        try:
            frame = self.page.frame_locator(frame_selector).first
            if not frame:
                raise ElementNotFoundError(f"IFrame with selector '{frame_selector}' not found")
            return frame
        except TimeoutError:
            raise ElementNotFoundError(f"IFrame with selector '{frame_selector}' not found")

    def upload_file(self, selector: str, file_paths: Union[str, List[str]]):
        """Upload one or multiple files"""
        self.page.locator(selector).set_input_files(file_paths)

    def wait_for_network_idle(self, timeout: int = 5000):
        """Wait for network connections to be idle"""
        self.page.wait_for_load_state('networkidle', timeout=timeout)

    def intercept_requests(self, url_pattern: str, callback):
        """Intercept network requests matching a URL pattern"""
        self.page.route(url_pattern, callback)

    def wait_for_response(self, url_pattern: str, timeout: int = 5000):
        """Wait for a specific response"""
        return self.page.wait_for_response(url_pattern, timeout=timeout)

    def new_page(self) -> Page:
        """Open a new tab/page"""
        return self.page.context.new_page()

    def switch_page(self, page_index: int) -> None:
        """Switch to a specific page by index"""
        pages = self.page.context.pages
        if 0 <= page_index < len(pages):
            self.page = pages[page_index]
        else:
            raise IndexError("Page index out of range")

    def get_local_storage(self, key: Optional[str] = None) -> Union[str, Dict]:
        """Get local storage data"""
        if key:
            return self.page.evaluate(f'localStorage.getItem("{key}")')
        return self.page.evaluate('JSON.stringify(localStorage)')

    def set_local_storage(self, key: str, value: str):
        """Set local storage data"""
        self.page.evaluate(f'localStorage.setItem("{key}", "{value}")')

    def clear_local_storage(self):
        """Clear all local storage data"""
        self.page.evaluate('localStorage.clear()')

    def handle_dialog(self, accept: bool = True, prompt_text: Optional[str] = None):
        """Handle JavaScript dialogs (alert, confirm, prompt)"""
        self.page.on('dialog', lambda dialog: dialog.accept(prompt_text) if accept else dialog.dismiss())

    def wait_for_download(self) -> str:
        """Wait for and handle file download"""
        with self.page.expect_download() as download_info:
            return download_info.value.path()

    def retry_with_timeout(self, action, max_retries: int = 3, timeout: int = 5000):
        """Retry an action with timeout"""
        for attempt in range(max_retries):
            try:
                return action()
            except TimeoutError as e:
                if attempt == max_retries - 1:
                    raise ActionTimeoutError(f"Action failed after {max_retries} attempts: {str(e)}")