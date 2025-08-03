import asyncio
import logging
from typing import Dict, Any, Optional, List
from playwright.async_api import async_playwright, Browser, Page
import json
import os
from datetime import datetime
import base64

logger = logging.getLogger(__name__)

class BrowserAutomationService:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        self.is_initialized = False

    async def initialize(self):
        """Initialize the browser automation service."""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            self.page = await self.context.new_page()
            self.is_initialized = True
            logger.info("Browser automation service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize browser automation service: {e}")
            raise

    async def cleanup(self):
        """Clean up browser resources."""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            self.is_initialized = False
            logger.info("Browser automation service cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a browser automation task."""
        if not self.is_initialized:
            await self.initialize()

        try:
            command = task_data.get("command", "")
            parameters = task_data.get("parameters", {})
            
            # Parse the command to determine action
            action = self._parse_command(command)
            
            if action == "navigate":
                return await self._navigate_to_url(parameters)
            elif action == "fill_form":
                return await self._fill_form(parameters)
            elif action == "click_element":
                return await self._click_element(parameters)
            elif action == "screenshot":
                return await self._take_screenshot(parameters)
            elif action == "make_workflow":
                return await self._create_make_workflow(parameters)
            elif action == "canva_design":
                return await self._create_canva_design(parameters)
            elif action == "extract_data":
                return await self._extract_data(parameters)
            else:
                raise ValueError(f"Unknown action: {action}")

        except Exception as e:
            logger.error(f"Error executing browser task: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def _parse_command(self, command: str) -> str:
        """Parse the command to determine the action type."""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ["go to", "navigate", "visit", "open"]):
            return "navigate"
        elif any(word in command_lower for word in ["fill", "form", "input", "type"]):
            return "fill_form"
        elif any(word in command_lower for word in ["click", "button", "link"]):
            return "click_element"
        elif any(word in command_lower for word in ["screenshot", "capture", "photo"]):
            return "screenshot"
        elif any(word in command_lower for word in ["make.com", "workflow", "automation"]):
            return "make_workflow"
        elif any(word in command_lower for word in ["canva", "design", "create design"]):
            return "canva_design"
        elif any(word in command_lower for word in ["extract", "scrape", "get data"]):
            return "extract_data"
        else:
            return "navigate"  # Default action

    async def _navigate_to_url(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Navigate to a specific URL."""
        try:
            url = parameters.get("url", "")
            if not url:
                raise ValueError("URL is required for navigation")

            await self.page.goto(url, wait_until="networkidle")
            
            # Wait for page to load
            await self.page.wait_for_load_state("domcontentloaded")
            
            title = await self.page.title()
            
            return {
                "success": True,
                "action": "navigate",
                "url": url,
                "title": title,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": "navigate"
            }

    async def _fill_form(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Fill a form with provided data."""
        try:
            form_data = parameters.get("form_data", {})
            selectors = parameters.get("selectors", {})
            
            for field_name, value in form_data.items():
                selector = selectors.get(field_name, f'[name="{field_name}"]')
                
                try:
                    # Try different selector strategies
                    element = await self.page.wait_for_selector(selector, timeout=5000)
                    if element:
                        await element.fill(str(value))
                        logger.info(f"Filled field {field_name} with value {value}")
                except Exception as e:
                    logger.warning(f"Could not fill field {field_name}: {e}")

            return {
                "success": True,
                "action": "fill_form",
                "fields_filled": list(form_data.keys()),
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Form filling error: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": "fill_form"
            }

    async def _click_element(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Click on an element."""
        try:
            selector = parameters.get("selector", "")
            if not selector:
                raise ValueError("Selector is required for clicking")

            await self.page.click(selector)
            
            return {
                "success": True,
                "action": "click_element",
                "selector": selector,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Click error: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": "click_element"
            }

    async def _take_screenshot(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Take a screenshot of the current page."""
        try:
            screenshot_path = f"screenshots/screenshot_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs("screenshots", exist_ok=True)
            
            screenshot_bytes = await self.page.screenshot(
                path=screenshot_path,
                full_page=parameters.get("full_page", True)
            )
            
            # Convert to base64 for API response
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            return {
                "success": True,
                "action": "screenshot",
                "screenshot_path": screenshot_path,
                "screenshot_base64": screenshot_base64,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": "screenshot"
            }

    async def _create_make_workflow(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Make.com workflow."""
        try:
            # Navigate to Make.com
            await self.page.goto("https://www.make.com/en/login")
            
            # Login (would need credentials in parameters)
            email = parameters.get("email")
            password = parameters.get("password")
            
            if email and password:
                await self.page.fill('input[type="email"]', email)
                await self.page.fill('input[type="password"]', password)
                await self.page.click('button[type="submit"]')
                
                # Wait for login
                await self.page.wait_for_load_state("networkidle")
            
            # Navigate to create new scenario
            await self.page.goto("https://www.make.com/en/scenarios")
            await self.page.click('button[data-testid="create-scenario-button"]')
            
            # Create workflow based on parameters
            workflow_config = parameters.get("workflow_config", {})
            # Implementation would depend on specific workflow requirements
            
            return {
                "success": True,
                "action": "make_workflow",
                "workflow_created": True,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Make.com workflow creation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": "make_workflow"
            }

    async def _create_canva_design(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Canva design."""
        try:
            # Navigate to Canva
            await self.page.goto("https://www.canva.com/")
            
            # Click on create design
            await self.page.click('button[data-testid="create-design-button"]')
            
            # Select template type
            template_type = parameters.get("template_type", "presentation")
            await self.page.click(f'[data-testid="{template_type}-template"]')
            
            # Customize design based on parameters
            design_config = parameters.get("design_config", {})
            # Implementation would depend on specific design requirements
            
            return {
                "success": True,
                "action": "canva_design",
                "design_created": True,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Canva design creation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": "canva_design"
            }

    async def _extract_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data from the current page."""
        try:
            selectors = parameters.get("selectors", {})
            extracted_data = {}
            
            for data_name, selector in selectors.items():
                try:
                    element = await self.page.query_selector(selector)
                    if element:
                        text_content = await element.text_content()
                        extracted_data[data_name] = text_content.strip()
                except Exception as e:
                    logger.warning(f"Could not extract {data_name}: {e}")
            
            return {
                "success": True,
                "action": "extract_data",
                "extracted_data": extracted_data,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Data extraction error: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": "extract_data"
            }

    async def get_page_info(self) -> Dict[str, Any]:
        """Get information about the current page."""
        try:
            if not self.page:
                return {"error": "No page loaded"}

            title = await self.page.title()
            url = self.page.url
            
            return {
                "title": title,
                "url": url,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting page info: {e}")
            return {"error": str(e)}