import logging
from typing import Dict, Optional
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import json

from . import static_scraping_data


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GMGNScraper:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.api_responses: Dict = {}

    async def __aenter__(self) -> 'GMGNScraper':
        await self.init_browser()
        return self

    async def __aexit__(self, *_) -> None:
        await self.cleanup()

    async def init_browser(self) -> None:
        """Initialize Playwright browser"""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.firefox.launch(headless=True)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            logger.info('Browser initialized successfully')
        except Exception as e:
            logger.error(f'Failed to initialize browser: {str(e)}')
            await self.cleanup()
            raise

    async def intercept_api_responses(self, token_address: str) -> None:
        """Intercept and store API responses"""
        if not self.page or not self.context:
            raise RuntimeError('Browser not initialized')

        async def handle_response(response):
            try:
                is_api_url = response.url.startswith(static_scraping_data.api_base_url)
                is_defi_url = response.url.startswith(
                    static_scraping_data.defi_base_url
                )

                if (is_api_url or is_defi_url) and any(
                    endpoint in response.url
                    for endpoint in static_scraping_data.expected_endpoints
                ):
                    json_data = await response.json()
                    self.api_responses[response.url] = {
                        'data': json_data,
                    }
                    logger.info(f'Intercepted API response from: {response.url}')
            except json.JSONDecodeError:
                logger.error(f'Invalid JSON in response: {response.url}')
            except Exception as e:
                logger.error(f'Error handling response: {str(e)}')

        self.page.on('response', handle_response)

        token_url = (
            f'{static_scraping_data.client_base_url}/{token_address}?tab=holders'
        )
        await self.page.goto(token_url, wait_until='networkidle')

        await asyncio.sleep(5)

    async def get_token_data(self, token_address: str) -> Dict:
        """Get token data by intercepting API responses"""
        results = {}
        try:
            await self.intercept_api_responses(token_address)

            for endpoint in static_scraping_data.expected_endpoints:
                found = False
                for url in self.api_responses:
                    if endpoint in url:
                        results[endpoint] = self.api_responses[url]['data']
                        found = True
                        break
                if not found:
                    logger.warning(f'Missing endpoint: {endpoint}')

            return results

        except Exception as e:
            logger.error(f'Error getting token data: {str(e)}')
            raise

    async def cleanup(self) -> None:
        """Cleanup browser resources"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            logger.info('Browser cleanup completed')
        except Exception as e:
            logger.error(f'Error during cleanup: {str(e)}')
