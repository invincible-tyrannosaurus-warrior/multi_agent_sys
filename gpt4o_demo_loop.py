from playwright.async_api import async_playwright, TimeoutError
import asyncio
import time

async def capture_debug_info(page, step_name):
    """Capture screenshot and HTML for debugging purposes"""
    try:
        current_page = await get_current_active_page(page.context)
        screenshot_path = f"debug_{step_name}_{int(time.time())}.png"
        await current_page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved: {screenshot_path}")

        html_path = f"debug_{step_name}_{int(time.time())}.txt"
        content = await current_page.content()
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"HTML content saved as text: {html_path}")

        return screenshot_path, html_path
    except Exception as e:
        print(f"Failed to capture debug info: {e}")
        return None, None

async def get_current_active_page(context):
    """Get the most recently created/active page from browser context"""
    pages = context.pages
    if pages:
        return pages[-1]
    else:
        return await context.new_page()

async def safe_wait_and_click(page, selector, step_description, timeout=30000):
    """Safely wait for element and click with debugging"""
    try:
        current_page = await get_current_active_page(page.context)
        
        print(f"Looking for: {step_description}")
        element = current_page.locator(selector).first
        await element.wait_for(state='visible', timeout=timeout)
        await element.click()
        print(f"Successfully clicked: {step_description}")
        
        await asyncio.sleep(1)  # Small wait for potential navigation
        
        new_current_page = await get_current_active_page(page.context)
        if new_current_page != current_page:
            print(f"New page detected after clicking {step_description}")
        
        return True, new_current_page
    except Exception as e:
        print(f"Failed to find/click {step_description}: {e}")
        current_page = await get_current_active_page(page.context)
        await capture_debug_info(current_page, step_description.replace(' ', '_').lower())
        return False, current_page

async def run(playwright):
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        await page.goto("https://aio.autoliv.com")
        await page.wait_for_load_state("networkidle")

        # It might be necessary to scroll or navigate tabs to find the 'Workflow' tile.
        # Investigate potential tabs or ensure element focus.
        tiles_selector = "div.app-grid div:has-text('Workflow')"
        success, page = await safe_wait_and_click(page, tiles_selector, "Workflow tile")
        if not success:
            print("Attempting alternative navigation to find 'Workflow'")
            # Add logic here if the tile is under a different section/tab.

        if success:
            page = await get_current_active_page(context)
            await page.wait_for_load_state("networkidle")

            # Check other elements if the logic above is bypassed:
            success, page = await safe_wait_and_click(page, "button:has-text('Task Management')", "Task Management dropdown")
            if success:
                page = await get_current_active_page(context)

            success, page = await safe_wait_and_click(page, "text=Initiate Task", "Initiate Task dropdown option")
            if success:
                page = await get_current_active_page(context)
                await page.wait_for_load_state("networkidle")

            success, page = await safe_wait_and_click(page, "text=Travel And Expense", "Travel And Expense category")
            if success:
                page = await get_current_active_page(context)

            success, page = await safe_wait_and_click(page, "text=New Employee Expense Claim", "New Employee Expense Claim process")
            if success:
                page = await get_current_active_page(context)
                await page.wait_for_load_state("networkidle")

            success, page = await safe_wait_and_click(page, "text=Add Expense Claim Item", "Add Expense Claim Item button")
            if success:
                page = await get_current_active_page(context)
                await page.wait_for_load_state("networkidle")

            success, page = await safe_wait_and_click(page, "text=Account", "Account dropdown")
            if success:
                page = await get_current_active_page(context)

            account_option_selector = "text=2609 - Other expenses for domestic travel and local travel"
            success, page = await safe_wait_and_click(page, account_option_selector, "Account option")
    
    except Exception as e:
        print(f"Script failed: {e}")
        current_page = await get_current_active_page(context)
        await capture_debug_info(current_page, "final_error")
    finally:
        await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == "__main__":
    asyncio.run(main())