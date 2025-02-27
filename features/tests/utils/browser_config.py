from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Generator

class BrowserConfig:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def setup_browser(self, headless: bool = False) -> None:
        """Initialize browser with specified configuration"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=['--start-maximized']
        )

    def create_context(self) -> BrowserContext:
        """Create a new browser context with default viewport"""
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        return self.context

    def create_page(self) -> Page:
        """Create a new page in the current context"""
        self.page = self.context.new_page()
        return self.page

    def close_context(self) -> None:
        """Close the current browser context"""
        if self.context:
            self.context.close()

    def close_browser(self) -> None:
        """Close browser and stop playwright"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def get_page(self) -> Page:
        """Get the current page instance"""
        return self.page