import random
import asyncio
from playwright.async_api import async_playwright
from fake_useragent import UserAgent

async def load_website(url, scrolls=6):
    ua = UserAgent()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )

        context = await browser.new_context(
            user_agent=ua.random,
            viewport=None
        )

        page = await context.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")

        # Human-like scrolling
        for _ in range(scrolls):
            await page.mouse.wheel(0, random.randint(2000, 4000))
            await page.wait_for_timeout(random.randint(1500, 3000))

        html = await page.content()
        await browser.close()
        return html
