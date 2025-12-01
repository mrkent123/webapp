#!/usr/bin/env python3
"""
Mobile UI Testing Suite for eTax Mobile PWA
Tests UI across multiple devices and screen sizes
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

# Test configuration
PWA_URL = "file:///workspace/webapp"
OUTPUT_DIR = Path("/workspace/test-results")

# Device configurations for testing
DEVICES = [
    {"name": "iPhone 12", "width": 390, "height": 844, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"},
    {"name": "iPhone 12 Pro Max", "width": 428, "height": 926, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"},
    {"name": "Samsung Galaxy S21", "width": 360, "height": 800, "user_agent": "Mozilla/5.0 (Linux; Android 11; SM-G991B)"},
    {"name": "iPad Pro", "width": 1024, "height": 768, "user_agent": "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)"},
    {"name": "Samsung Galaxy Tab S7", "width": 1600, "height": 2560, "user_agent": "Mozilla/5.0 (Linux; Android 11; SM-T870)"},
    {"name": "Desktop HD", "width": 1920, "height": 1080, "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
]

# Pages to test
TEST_PAGES = [
    ("login", "login.html"),
    ("home", "home.html"),
    ("bien-lai", "pages/bien-lai-dien-tu.html"),
    ("hoa-don", "pages/hoa-don-dien-tu.html"),
]

async def test_device_compatibility():
    """Test PWA UI across multiple device types"""
    async with async_playwright() as p:
        print("🚀 Starting Mobile UI Testing Suite for eTax Mobile PWA")
        
        # Create output directory
        OUTPUT_DIR.mkdir(exist_ok=True)
        (OUTPUT_DIR / "screenshots").mkdir(exist_ok=True)
        (OUTPUT_DIR / "reports").mkdir(exist_ok=True)
        
        results = []
        
        for device in DEVICES:
            print(f"\n📱 Testing on {device['name']} ({device['width']}x{device['height']})")
            
            # Launch browser with device emulation
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            context = await browser.new_context(
                viewport={"width": device["width"], "height": device["height"]},
                user_agent=device["user_agent"],
                is_mobile=device["width"] < 768,
                has_touch=device["width"] < 768
            )
            
            page = await context.new_page()
            
            device_results = []
            
            for page_name, page_path in TEST_PAGES:
                try:
                    url = f"{PWA_URL}/{page_path}"
                    print(f"  🌐 Testing {page_name} page...")
                    
                    # Navigate to page
                    await page.goto(url, wait_until="networkidle")
                    await page.wait_for_timeout(2000)
                    
                    # Take screenshot
                    screenshot_path = OUTPUT_DIR / "screenshots" / f"{device['name'].replace(' ', '_')}_{page_name}.png"
                    await page.screenshot(
                        path=str(screenshot_path),
                        full_page=True,
                        animations="disabled"
                    )
                    
                    # Check for common UI elements
                    ui_checks = await check_ui_elements(page, page_name)
                    
                    device_results.append({
                        "page": page_name,
                        "url": url,
                        "screenshot": str(screenshot_path),
                        "ui_checks": ui_checks,
                        "viewport": f"{device['width']}x{device['height']}"
                    })
                    
                    print(f"    ✅ {page_name} - Screenshot saved")
                    
                except Exception as e:
                    print(f"    ❌ {page_name} - Error: {str(e)}")
                    device_results.append({
                        "page": page_name,
                        "error": str(e),
                        "viewport": f"{device['width']}x{device['height']}"
                    })
            
            await browser.close()
            
            results.append({
                "device": device["name"],
                "viewport": f"{device['width']}x{device['height']}",
                "results": device_results
            })
        
        # Generate test report
        await generate_test_report(results)
        await run_visual_comparison(results)
        
        print(f"\n🎉 Testing completed! Results saved in {OUTPUT_DIR}")
        return results

async def check_ui_elements(page, page_name):
    """Check for common UI elements and PWA features"""
    checks = {}
    
    try:
        # PWA theme color check
        theme_color = await page.evaluate("""
            () => {
                const meta = document.querySelector('meta[name="theme-color"]');
                return meta ? meta.content : 'Not found';
            }
        """)
        checks["theme_color"] = theme_color
        
        # Manifest check
        manifest = await page.evaluate("""
            () => {
                const link = document.querySelector('link[rel="manifest"]');
                return link ? link.href : 'Not found';
            }
        """)
        checks["manifest"] = manifest
        
        # Viewport meta check
        viewport = await page.evaluate("""
            () => {
                const meta = document.querySelector('meta[name="viewport"]');
                return meta ? meta.content : 'Not found';
            }
        """)
        checks["viewport"] = viewport
        
        # Page-specific checks
        if page_name == "login":
            # Check login form elements
            checks["login_form"] = await page.query_selector("form") is not None
            checks["username_field"] = await page.query_selector('input[type="text"], input[name*="mst"]') is not None
            checks["password_field"] = await page.query_selector('input[type="password"]') is not None
            checks["login_button"] = await page.query_selector('button[type="submit"], input[type="submit"]') is not None
            
        elif page_name == "home":
            # Check dashboard elements
            checks["sidebar"] = await page.query_selector(".sidebar") is not None
            checks["service_grid"] = await page.query_selector(".service-grid, .grid, [class*='service']") is not None
            checks["profile_section"] = await page.query_selector(".profile, [class*='profile'], [class*='user']") is not None
            
    except Exception as e:
        checks["error"] = str(e)
    
    return checks

async def generate_test_report(results):
    """Generate comprehensive test report"""
    report_path = OUTPUT_DIR / "reports" / "mobile-ui-test-report.html"
    
    html_report = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>eTax Mobile PWA - UI Test Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: #C60000; color: white; padding: 20px; border-radius: 8px; }}
            .device {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }}
            .page {{ margin: 10px 0; padding: 10px; background: #f9f9f9; border-radius: 4px; }}
            .success {{ color: #28a745; }}
            .error {{ color: #dc3545; }}
            .screenshot {{ max-width: 300px; border: 1px solid #ddd; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 eTax Mobile PWA - Mobile UI Test Report</h1>
            <p>Generated: {asyncio.get_event_loop().time()}</p>
        </div>
    """
    
    for device_result in results:
        html_report += f"""
        <div class="device">
            <h2>📱 {device_result['device']}</h2>
            <p><strong>Viewport:</strong> {device_result['viewport']}</p>
        """
        
        for page_result in device_result['results']:
            if 'error' in page_result:
                html_report += f"""
                <div class="page">
                    <h3>{page_result['page']}</h3>
                    <p class="error">❌ Error: {page_result['error']}</p>
                </div>
                """
            else:
                html_report += f"""
                <div class="page">
                    <h3>{page_result['page']}</h3>
                    <p><strong>URL:</strong> {page_result['url']}</p>
                    <img src="../screenshots/{device_result['device'].replace(' ', '_')}_{page_result['page']}.png" class="screenshot" alt="Screenshot">
                    <h4>UI Checks:</h4>
                    <ul>
                """
                
                for check, value in page_result['ui_checks'].items():
                    status = "✅" if value else "❌"
                    html_report += f"<li>{check}: {status} {value}</li>"
                
                html_report += """
                    </ul>
                </div>
                """
        
        html_report += "</div>"
    
    html_report += """
    </body>
    </html>
    """
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"📊 Test report generated: {report_path}")

async def run_visual_comparison(results):
    """Run visual comparison analysis"""
    print("\n🔍 Running Visual Comparison Analysis...")
    
    # Compare login page across devices
    login_screenshots = []
    for device_result in results:
        for page_result in device_result['results']:
            if page_result.get('page') == 'login' and 'screenshot' in page_result:
                login_screenshots.append({
                    'device': device_result['device'],
                    'path': page_result['screenshot']
                })
    
    if login_screenshots:
        print(f"📸 Found {len(login_screenshots)} login page screenshots for comparison")
        
        # Create comparison summary
        comparison_report = OUTPUT_DIR / "reports" / "visual-comparison.md"
        with open(comparison_report, 'w', encoding='utf-8') as f:
            f.write("# Visual Comparison Report\n\n")
            f.write("## Login Page Screenshots Comparison\n\n")
            for shot in login_screenshots:
                f.write(f"- **{shot['device']}**: {shot['path']}\n")
            f.write(f"\n## Summary\nTotal screenshots: {len(login_screenshots)}\n")
        
        print(f"📊 Visual comparison report: {comparison_report}")

if __name__ == "__main__":
    print("🎯 eTax Mobile PWA - Mobile UI Testing Suite")
    print("=" * 50)
    
    # Run the tests
    asyncio.run(test_device_compatibility())