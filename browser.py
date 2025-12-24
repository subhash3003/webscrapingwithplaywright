import random
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent

def load_website(url, scrolls=6):
    ua = UserAgent()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )

        context = browser.new_context(
            user_agent=ua.random,
            viewport=None
        )

        page = context.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")

        # Human-like scrolling
        for _ in range(scrolls):
            page.mouse.wheel(0, random.randint(2000, 4000))
            page.wait_for_timeout(random.randint(1500, 3000))

        html = page.content()
        browser.close()
        return html
