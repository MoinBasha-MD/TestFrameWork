from datetime import datetime
import os
from pathlib import Path
import re

class ScreenshotManager:
    def __init__(self, base_dir="screenshots"):
        self.base_dir = Path(base_dir)
        self.error_dir = self.base_dir / "errors"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure that the screenshot directories exist."""
        self.base_dir.mkdir(exist_ok=True)
        self.error_dir.mkdir(exist_ok=True)
    
    def _get_timestamp(self):
        """Generate a timestamp for the screenshot filename."""
        return datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    def _sanitize_filename(self, filename):
        """Sanitize the filename by replacing invalid characters with underscores."""
        # Replace any character that's not alphanumeric, dash, underscore, or dot with underscore
        sanitized = re.sub(r'[^\w\-\.]', '_', filename)
        # Remove any double underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        return sanitized
    
    def take_step_screenshot(self, context, step_name):
        """Take a screenshot after each step execution."""
        timestamp = self._get_timestamp()
        feature_name = self._sanitize_filename(context.feature.name)
        scenario_name = self._sanitize_filename(context.scenario.name)
        step_name = self._sanitize_filename(step_name)
        
        # Create feature and scenario directories
        feature_dir = self.base_dir / feature_name
        scenario_dir = feature_dir / scenario_name
        feature_dir.mkdir(exist_ok=True)
        scenario_dir.mkdir(exist_ok=True)
        
        # Generate screenshot filename
        filename = f"{step_name}_{timestamp}.png"
        screenshot_path = scenario_dir / filename
        
        # Take screenshot
        context.page.screenshot(path=str(screenshot_path))
        
    def take_error_screenshot(self, context, step_name):
        """Take a screenshot when a step fails."""
        timestamp = self._get_timestamp()
        feature_name = self._sanitize_filename(context.feature.name)
        scenario_name = self._sanitize_filename(context.scenario.name)
        step_name = self._sanitize_filename(step_name)
        
        # Generate error screenshot filename
        filename = f"ERROR_{feature_name}_{scenario_name}_{step_name}_{timestamp}.png"
        screenshot_path = self.error_dir / filename
        
        # Take screenshot
        context.page.screenshot(path=str(screenshot_path))