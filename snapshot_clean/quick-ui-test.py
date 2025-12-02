#!/usr/bin/env python3
"""
Simple UI Test Demo for eTax Mobile PWA
Basic screenshot and UI validation test
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def quick_ui_test():
    """Quick UI test for demonstration"""
    print("🧪 Quick UI Test Demo for eTax Mobile PWA")
    print("=" * 50)
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        
        # Test login page
        print("📱 Testing login page...")
        context = await browser.new_context(
            viewport={"width": 375, "height": 667, "isMobile": True}
        )
        page = await context.new_page()
        
        try:
            await page.goto("file:///workspace/webapp/login.html", wait_until="networkidle")
            await page.wait_for_timeout(2000)
            
            # Take screenshot
            screenshot_path = "/workspace/test-results/demo-login.png"
            Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=screenshot_path)
            
            # Check for key elements
            ui_elements = await page.evaluate("""
                () => {
                    return {
                        title: document.title,
                        has_form: !!document.querySelector('form'),
                        has_mst_field: !!document.querySelector('input[type="text"], input[name*="mst"]'),
                        has_password_field: !!document.querySelector('input[type="password"]'),
                        has_login_button: !!document.querySelector('button[type="submit"], input[type="submit"]'),
                        theme_color: document.querySelector('meta[name="theme-color"]')?.content || 'Not found',
                        has_viewport: !!document.querySelector('meta[name="viewport"]')
                    };
                }
            """)
            
            print("✅ Login page test completed!")
            print(f"📊 Title: {ui_elements['title']}")
            print(f"🎨 Theme Color: {ui_elements['theme_color']}")
            print(f"📝 Has Form: {ui_elements['has_form']}")
            print(f"🔤 Has MST Field: {ui_elements['has_mst_field']}")
            print(f"🔒 Has Password Field: {ui_elements['has_password_field']}")
            print(f"🔘 Has Login Button: {ui_elements['has_login_button']}")
            print(f"📱 Has Viewport: {ui_elements['has_viewport']}")
            print(f"📸 Screenshot saved: {screenshot_path}")
            
        except Exception as e:
            print(f"❌ Login page test failed: {str(e)}")
        
        await browser.close()
        
        print("\n🎉 Quick UI test demo completed!")

if __name__ == "__main__":
    asyncio.run(quick_ui_test())