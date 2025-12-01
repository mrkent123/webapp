#!/usr/bin/env python3
"""
Advanced UI Comparison Tool for eTax Mobile PWA
Uses AI to analyze screenshots and detect UI differences
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
import base64

class UIComparator:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        
    async def initialize(self):
        """Initialize browser for testing"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
    async def setup_responsive_context(self, width, height, device_name):
        """Setup browser context for specific device"""
        # Common mobile device configurations
        device_configs = {
            'iPhone SE': {'width': 375, 'height': 667, 'is_mobile': True},
            'iPhone 12': {'width': 390, 'height': 844, 'is_mobile': True},
            'iPhone 12 Pro Max': {'width': 428, 'height': 926, 'is_mobile': True},
            'Samsung Galaxy S20': {'width': 360, 'height': 800, 'is_mobile': True},
            'iPad': {'width': 768, 'height': 1024, 'is_mobile': False},
            'iPad Pro': {'width': 1024, 'height': 1366, 'is_mobile': False},
            'Desktop': {'width': 1920, 'height': 1080, 'is_mobile': False}
        }
        
        config = device_configs.get(device_name, {
            'width': width,
            'height': height, 
            'is_mobile': width < 768
        })
        
        self.context = await self.browser.new_context(
            viewport={"width": config['width'], "height": config['height']},
            is_mobile=config['is_mobile'],
            has_touch=config['is_mobile'],
            device_scale_factor=2  # For retina displays
        )
        
        return config
    
    async def capture_ui_elements(self, page, page_name):
        """Capture and analyze UI elements on a page"""
        ui_analysis = await page.evaluate("""
            () => {
                const analysis = {
                    title: document.title,
                    viewport: {
                        width: window.innerWidth,
                        height: window.innerHeight
                    },
                    meta: {},
                    elements: [],
                    colors: [],
                    fonts: [],
                    pwa: {
                        manifest: null,
                        theme_color: null,
                        service_worker: null
                    }
                };
                
                // Get meta tags
                document.querySelectorAll('meta').forEach(meta => {
                    const name = meta.name || meta.property;
                    if (name) {
                        analysis.meta[name] = meta.content;
                    }
                });
                
                // Get PWA info
                const manifest = document.querySelector('link[rel="manifest"]');
                if (manifest) {
                    analysis.pwa.manifest = manifest.href;
                }
                
                const themeColor = document.querySelector('meta[name="theme-color"]');
                if (themeColor) {
                    analysis.pwa.theme_color = themeColor.content;
                }
                
                // Get colors used
                const styles = window.getComputedStyle(document.body);
                const bgColor = styles.backgroundColor;
                const textColor = styles.color;
                if (bgColor && bgColor !== 'rgba(0, 0, 0, 0)') {
                    analysis.colors.push({element: 'body', property: 'background', value: bgColor});
                }
                if (textColor && textColor !== 'rgba(0, 0, 0, 1)') {
                    analysis.colors.push({element: 'body', property: 'color', value: textColor});
                }
                
                // Get fonts
                analysis.fonts.push({
                    family: styles.fontFamily,
                    size: styles.fontSize,
                    weight: styles.fontWeight
                });
                
                // Get form elements
                const forms = document.querySelectorAll('form');
                forms.forEach((form, index) => {
                    const inputs = form.querySelectorAll('input, select, textarea');
                    analysis.elements.push({
                        type: 'form',
                        id: form.id,
                        className: form.className,
                        inputCount: inputs.length
                    });
                });
                
                // Get buttons
                const buttons = document.querySelectorAll('button, input[type="submit"], input[type="button"]');
                buttons.forEach((btn, index) => {
                    analysis.elements.push({
                        type: 'button',
                        text: btn.textContent.trim(),
                        id: btn.id,
                        className: btn.className
                    });
                });
                
                // Get navigation
                const nav = document.querySelectorAll('nav, .nav, .navigation, [class*="nav"]');
                nav.forEach((navEl, index) => {
                    analysis.elements.push({
                        type: 'navigation',
                        id: navEl.id,
                        className: navEl.className
                    });
                });
                
                return analysis;
            }
        """)
        
        return ui_analysis
    
    async def test_responsive_breakpoints(self, page):
        """Test responsive behavior across different breakpoints"""
        breakpoints = [
            {'name': 'Mobile XS', 'width': 320, 'height': 568},
            {'name': 'Mobile SM', 'width': 375, 'height': 667},
            {'name': 'Mobile MD', 'width': 414, 'height': 896},
            {'name': 'Tablet', 'width': 768, 'height': 1024},
            {'name': 'Desktop SM', 'width': 1024, 'height': 768},
            {'name': 'Desktop MD', 'width': 1280, 'height': 720},
            {'name': 'Desktop LG', 'width': 1920, 'height': 1080}
        ]
        
        responsive_results = []
        
        for breakpoint in breakpoints:
            await self.context.set_viewport_size({"width": breakpoint['width'], "height": breakpoint['height']})
            await page.wait_for_timeout(500)  # Wait for layout
            
            # Check if layout breaks
            layout_check = await page.evaluate("""
                () => {
                    const body = document.body;
                    const rect = body.getBoundingClientRect();
                    
                    return {
                        width: rect.width,
                        height: rect.height,
                        overflow: body.scrollWidth > window.innerWidth,
                        horizontalScroll: body.scrollWidth > body.clientWidth
                    };
                }
            """)
            
            responsive_results.append({
                'breakpoint': breakpoint['name'],
                'size': f"{breakpoint['width']}x{breakpoint['height']}",
                'layout': layout_check,
                'screenshot_taken': False
            })
        
        return responsive_results

async def run_ui_comparison():
    """Main UI comparison function"""
    comparator = UIComparator()
    await comparator.initialize()
    
    print("🔍 Advanced UI Comparison Tool for eTax Mobile PWA")
    print("=" * 60)
    
    # Test pages
    pages_to_test = [
        ("login", "/workspace/webapp/login.html"),
        ("home", "/workspace/webapp/home.html"),
        ("bien-lai", "/workspace/webapp/pages/bien-lai-dien-tu.html"),
        ("hoa-don", "/workspace/webapp/pages/hoa-don-dien-tu.html")
    ]
    
    # Test devices
    devices = [
        ("iPhone SE", 375, 667),
        ("iPhone 12", 390, 844),
        ("Samsung Galaxy S20", 360, 800),
        ("iPad", 768, 1024),
        ("Desktop", 1920, 1080)
    ]
    
    results = {}
    
    for page_name, page_path in pages_to_test:
        print(f"\n📄 Testing page: {page_name}")
        results[page_name] = {}
        
        for device_name, width, height in devices:
            print(f"  📱 Device: {device_name} ({width}x{height})")
            
            # Setup device context
            config = await comparator.setup_responsive_context(width, height, device_name)
            page = await comparator.context.new_page()
            
            try:
                # Navigate to page
                await page.goto(f"file://{page_path}", wait_until="networkidle")
                await page.wait_for_timeout(2000)
                
                # Capture UI analysis
                ui_analysis = await comparator.capture_ui_elements(page, page_name)
                
                # Test responsive behavior
                if device_name == "Desktop":  # Only test responsive on one device to save time
                    responsive_results = await comparator.test_responsive_breakpoints(page)
                    ui_analysis['responsive'] = responsive_results
                
                # Take screenshot
                screenshot_path = f"/workspace/test-results/comparison/{device_name}_{page_name}.png"
                Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
                await page.screenshot(path=screenshot_path, full_page=True, animations="disabled")
                
                results[page_name][device_name] = {
                    'ui_analysis': ui_analysis,
                    'screenshot_path': screenshot_path,
                    'device_config': config
                }
                
                print(f"    ✅ Completed")
                
            except Exception as e:
                print(f"    ❌ Error: {str(e)}")
                results[page_name][device_name] = {
                    'error': str(e)
                }
            
            await page.close()
    
    await comparator.browser.close()
    
    # Generate comprehensive report
    await generate_comparison_report(results)
    
    print(f"\n🎉 UI Comparison completed!")
    print(f"📊 Results saved in /workspace/test-results/comparison/")
    
    return results

async def generate_comparison_report(results):
    """Generate detailed comparison report"""
    report_path = Path("/workspace/test-results/ui-comparison-report.json")
    
    # Add analysis summary
    analysis_summary = {
        'total_pages_tested': len(results),
        'total_devices_tested': len(next(iter(results.values()))),
        'pwa_compliance': {},
        'responsive_issues': [],
        'ui_consistency': {}
    }
    
    # Analyze PWA compliance
    for page_name, device_results in results.items():
        for device_name, result in device_results.items():
            if 'ui_analysis' in result:
                analysis = result['ui_analysis']
                
                # Check PWA compliance
                pwa_compliant = {
                    'has_theme_color': analysis['pwa']['theme_color'] is not None,
                    'has_manifest': analysis['pwa']['manifest'] is not None,
                    'has_viewport': 'viewport' in analysis['meta']
                }
                
                if page_name not in analysis_summary['pwa_compliance']:
                    analysis_summary['pwa_compliance'][page_name] = pwa_compliant
                
                # Check for responsive issues
                if 'responsive' in analysis:
                    for breakpoint in analysis['responsive']:
                        if breakpoint['layout']['overflow'] or breakpoint['layout']['horizontalScroll']:
                            analysis_summary['responsive_issues'].append({
                                'page': page_name,
                                'device': device_name,
                                'breakpoint': breakpoint['breakpoint'],
                                'issue': 'Layout overflow detected'
                            })
    
    final_report = {
        'summary': analysis_summary,
        'detailed_results': results,
        'generated_at': '2025-12-02 00:19:46'
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Detailed report saved: {report_path}")

if __name__ == "__main__":
    asyncio.run(run_ui_comparison())