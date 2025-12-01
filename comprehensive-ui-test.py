#!/usr/bin/env python3
"""
Comprehensive UI Testing Suite for eTax Mobile PWA
Focus on accurate pixel measurements and responsive analysis
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

class DetailedUITester:
    def __init__(self):
        self.results = {}
        
    async def test_precise_measurements(self, page):
        """Test with precise pixel measurements"""
        print("📏 Testing Precise UI Measurements...")
        
        measurements = await page.evaluate("""
            () => {
                const data = {
                    viewport: {
                        width: window.innerWidth,
                        height: window.innerHeight,
                        devicePixelRatio: window.devicePixelRatio
                    },
                    document: {
                        width: document.documentElement.clientWidth,
                        height: document.documentElement.clientHeight,
                        scrollWidth: document.documentElement.scrollWidth,
                        scrollHeight: document.documentElement.scrollHeight
                    },
                    body: {
                        width: document.body.clientWidth,
                        height: document.body.clientHeight,
                        offsetWidth: document.body.offsetWidth,
                        offsetHeight: document.body.offsetHeight,
                        scrollWidth: document.body.scrollWidth,
                        scrollHeight: document.body.scrollHeight
                    },
                    elements: {}
                };
                
                // Measure key elements precisely
                const elements = [
                    'meta[name="viewport"]',
                    'meta[name="theme-color"]', 
                    'link[rel="manifest"]',
                    'form',
                    'input[type="text"]',
                    'input[type="password"]',
                    'button[type="submit"]',
                    '.sidebar',
                    '.service-grid'
                ];
                
                elements.forEach(selector => {
                    const el = document.querySelector(selector);
                    if (el) {
                        const rect = el.getBoundingClientRect();
                        const style = window.getComputedStyle(el);
                        data.elements[selector] = {
                            exists: true,
                            dimensions: {
                                width: rect.width,
                                height: rect.height,
                                top: rect.top,
                                left: rect.left,
                                bottom: rect.bottom,
                                right: rect.right
                            },
                            position: {
                                offsetTop: el.offsetTop,
                                offsetLeft: el.offsetLeft,
                                offsetWidth: el.offsetWidth,
                                offsetHeight: el.offsetHeight
                            },
                            style: {
                                display: style.display,
                                position: style.position,
                                overflow: style.overflow,
                                overflowX: style.overflowX,
                                overflowY: style.overflowY,
                                visibility: style.visibility,
                                opacity: style.opacity,
                                zIndex: style.zIndex
                            },
                            computedColor: {
                                backgroundColor: style.backgroundColor,
                                color: style.color,
                                borderColor: style.borderColor
                            }
                        };
                    } else {
                        data.elements[selector] = { exists: false };
                    }
                });
                
                // Check for responsive issues
                data.responsiveIssues = {
                    hasHorizontalScroll: document.body.scrollWidth > document.body.clientWidth,
                    hasVerticalScroll: document.body.scrollHeight > document.body.clientHeight,
                    overflowX: document.body.style.overflowX !== 'hidden' && document.body.scrollWidth > document.body.clientWidth,
                    overflowY: document.body.style.overflowY !== 'hidden' && document.body.scrollHeight > document.body.clientHeight
                };
                
                return data;
            }
        """)
        
        return measurements
    
    async def test_responsive_breakpoints_detailed(self, page):
        """Test responsive behavior with detailed analysis"""
        print("📱 Testing Detailed Responsive Breakpoints...")
        
        # Standard breakpoints
        breakpoints = [
            {'name': 'XS Mobile', 'width': 320, 'height': 568},
            {'name': 'Small Mobile', 'width': 375, 'height': 667},
            {'name': 'Large Mobile', 'width': 414, 'height': 896},
            {'name': 'Tablet Portrait', 'width': 768, 'height': 1024},
            {'name': 'Tablet Landscape', 'width': 1024, 'height': 768},
            {'name': 'Desktop Small', 'width': 1280, 'height': 720},
            {'name': 'Desktop Large', 'width': 1920, 'height': 1080}
        ]
        
        breakpoint_results = []
        
        for breakpoint in breakpoints:
            print(f"  🔍 Testing {breakpoint['name']} ({breakpoint['width']}x{breakpoint['height']})...")
            
            await page.set_viewport_size({"width": breakpoint['width'], "height": breakpoint['height']})
            await page.wait_for_timeout(1000)  # Wait for layout
            
            # Detailed layout analysis
            layout_analysis = await page.evaluate("""
                () => {
                    const body = document.body;
                    const html = document.documentElement;
                    
                    return {
                        viewport: {
                            width: window.innerWidth,
                            height: window.innerHeight
                        },
                        body: {
                            width: body.clientWidth,
                            height: body.clientHeight,
                            scrollWidth: body.scrollWidth,
                            scrollHeight: body.scrollHeight,
                            overflowX: body.scrollWidth > body.clientWidth,
                            overflowY: body.scrollHeight > body.clientHeight
                        },
                        html: {
                            width: html.clientWidth,
                            height: html.clientHeight,
                            scrollWidth: html.scrollWidth,
                            scrollHeight: html.scrollHeight
                        },
                        elements: {},
                        layout: {}
                    };
                }
            """)
            
            # Check specific UI elements at this breakpoint
            ui_elements_check = await page.evaluate("""
                () => {
                    const checks = {
                        sidebar: {
                            exists: !!document.querySelector('.sidebar'),
                            visible: false,
                            width: 0,
                            position: 'relative'
                        },
                        serviceGrid: {
                            exists: !!document.querySelector('.service-grid, [class*="grid"]'),
                            itemCount: 0,
                            columns: 1
                        },
                        forms: {
                            inputWidth: 0,
                            buttonWidth: 0,
                            formWidth: 0
                        }
                    };
                    
                    // Check sidebar
                    const sidebar = document.querySelector('.sidebar');
                    if (sidebar) {
                        const sidebarRect = sidebar.getBoundingClientRect();
                        const sidebarStyle = window.getComputedStyle(sidebar);
                        checks.sidebar = {
                            exists: true,
                            visible: sidebarRect.width > 0 && sidebarStyle.visibility !== 'hidden',
                            width: sidebarRect.width,
                            position: sidebarStyle.position,
                            transform: sidebarStyle.transform,
                            opacity: sidebarStyle.opacity
                        };
                    }
                    
                    // Check service grid
                    const serviceGrid = document.querySelector('.service-grid, [class*="grid"]');
                    if (serviceGrid) {
                        const items = serviceGrid.querySelectorAll('.service-item, .grid-item, a');
                        const gridStyle = window.getComputedStyle(serviceGrid);
                        checks.serviceGrid = {
                            exists: true,
                            itemCount: items.length,
                            columns: gridStyle.gridTemplateColumns ? gridStyle.gridTemplateColumns.split(' ').length : 1
                        };
                    }
                    
                    // Check forms
                    const input = document.querySelector('input[type="text"], input[type="password"]');
                    const button = document.querySelector('button, input[type="submit"]');
                    const form = document.querySelector('form');
                    
                    if (input) {
                        const inputRect = input.getBoundingClientRect();
                        checks.forms.inputWidth = inputRect.width;
                    }
                    
                    if (button) {
                        const buttonRect = button.getBoundingClientRect();
                        checks.forms.buttonWidth = buttonRect.width;
                    }
                    
                    if (form) {
                        const formRect = form.getBoundingClientRect();
                        checks.forms.formWidth = formRect.width;
                    }
                    
                    return checks;
                }
            """)
            
            # Determine if layout is problematic
            isProblematic = (
                layout_analysis['body']['overflowX'] or 
                layout_analysis['body']['overflowY'] or
                (layout_analysis['body']['width'] > breakpoint['width']) or
                (ui_elements_check['sidebar']['exists'] and ui_elements_check['sidebar']['width'] > breakpoint['width'])
            )
            
            breakpoint_results.append({
                'breakpoint': breakpoint['name'],
                'dimensions': f"{breakpoint['width']}x{breakpoint['height']}",
                'layout_analysis': layout_analysis,
                'ui_elements': ui_elements_check,
                'is_problematic': isProblematic,
                'issues': self._identify_responsive_issues(layout_analysis, ui_elements_check, breakpoint)
            })
            
            print(f"    ✅ {breakpoint['name']}: {'❌ ISSUES' if isProblematic else '✅ OK'}")
        
        return breakpoint_results
    
    def _identify_responsive_issues(self, layout_analysis, ui_elements, breakpoint):
        """Identify specific responsive issues"""
        issues = []
        
        # Check for horizontal overflow
        if layout_analysis['body']['overflowX']:
            overflow_pixels = layout_analysis['body']['scrollWidth'] - layout_analysis['body']['width']
            issues.append(f"Horizontal overflow: {overflow_pixels}px")
        
        # Check for vertical overflow
        if layout_analysis['body']['overflowY']:
            overflow_pixels = layout_analysis['body']['scrollHeight'] - layout_analysis['body']['height']
            issues.append(f"Vertical overflow: {overflow_pixels}px")
        
        # Check sidebar issues
        if ui_elements['sidebar']['exists']:
            if ui_elements['sidebar']['width'] > breakpoint['width']:
                issues.append(f"Sidebar too wide: {ui_elements['sidebar']['width']}px > {breakpoint['width']}px")
            if not ui_elements['sidebar']['visible']:
                issues.append("Sidebar not visible")
        
        # Check element sizes
        if ui_elements['forms']['inputWidth'] > 0:
            if ui_elements['forms']['inputWidth'] > breakpoint['width'] - 40:  # Account for margins
                issues.append(f"Input too wide: {ui_elements['forms']['inputWidth']}px")
        
        return issues
    
    async def test_form_elements_detailed(self, page):
        """Detailed form element testing"""
        print("📝 Testing Form Elements in Detail...")
        
        form_analysis = await page.evaluate("""
            () => {
                const forms = document.querySelectorAll('form');
                const analysis = {
                    forms: [],
                    inputs: [],
                    buttons: [],
                    validation: {}
                };
                
                // Analyze forms
                forms.forEach((form, index) => {
                    const formRect = form.getBoundingClientRect();
                    const formStyle = window.getComputedStyle(form);
                    
                    analysis.forms.push({
                        index: index,
                        id: form.id,
                        className: form.className,
                        action: form.action,
                        method: form.method,
                        dimensions: {
                            width: formRect.width,
                            height: formRect.height,
                            top: formRect.top,
                            left: formRect.left
                        },
                        style: {
                            position: formStyle.position,
                            display: formStyle.display,
                            flexDirection: formStyle.flexDirection,
                            alignItems: formStyle.alignItems,
                            justifyContent: formStyle.justifyContent,
                            padding: formStyle.padding,
                            margin: formStyle.margin,
                            backgroundColor: formStyle.backgroundColor,
                            border: formStyle.border,
                            borderRadius: formStyle.borderRadius
                        }
                    });
                });
                
                // Analyze inputs
                const inputs = document.querySelectorAll('input');
                inputs.forEach((input, index) => {
                    const inputRect = input.getBoundingClientRect();
                    const inputStyle = window.getComputedStyle(input);
                    const inputValidity = input.validity;
                    
                    analysis.inputs.push({
                        index: index,
                        type: input.type,
                        name: input.name,
                        id: input.id,
                        placeholder: input.placeholder,
                        required: input.required,
                        value: input.value,
                        dimensions: {
                            width: inputRect.width,
                            height: inputRect.height,
                            top: inputRect.top,
                            left: inputRect.left
                        },
                        style: {
                            fontSize: inputStyle.fontSize,
                            fontFamily: inputStyle.fontFamily,
                            fontWeight: inputStyle.fontWeight,
                            padding: inputStyle.padding,
                            margin: inputStyle.margin,
                            border: inputStyle.border,
                            borderRadius: inputStyle.borderRadius,
                            backgroundColor: inputStyle.backgroundColor,
                            color: inputStyle.color,
                            outline: inputStyle.outline
                        },
                        validity: {
                            valid: inputValidity.valid,
                            valueMissing: inputValidity.valueMissing,
                            typeMismatch: inputValidity.typeMismatch,
                            patternMismatch: inputValidity.patternMismatch,
                            tooLong: inputValidity.tooLong,
                            tooShort: inputValidity.tooShort,
                            rangeUnderflow: inputValidity.rangeUnderflow,
                            rangeOverflow: inputValidity.rangeOverflow,
                            stepMismatch: inputValidity.stepMismatch,
                            badInput: inputValidity.badInput
                        }
                    });
                });
                
                // Analyze buttons
                const buttons = document.querySelectorAll('button, input[type="submit"], input[type="button"]');
                buttons.forEach((button, index) => {
                    const buttonRect = button.getBoundingClientRect();
                    const buttonStyle = window.getComputedStyle(button);
                    
                    analysis.buttons.push({
                        index: index,
                        type: button.type,
                        text: button.textContent.trim(),
                        id: button.id,
                        className: button.className,
                        disabled: button.disabled,
                        dimensions: {
                            width: buttonRect.width,
                            height: buttonRect.height,
                            top: buttonRect.top,
                            left: buttonRect.left
                        },
                        style: {
                            fontSize: buttonStyle.fontSize,
                            fontFamily: buttonStyle.fontFamily,
                            fontWeight: buttonStyle.fontWeight,
                            padding: buttonStyle.padding,
                            margin: buttonStyle.margin,
                            backgroundColor: buttonStyle.backgroundColor,
                            color: buttonStyle.color,
                            border: buttonStyle.border,
                            borderRadius: buttonStyle.borderRadius,
                            cursor: buttonStyle.cursor
                        }
                    });
                });
                
                return analysis;
            }
        """)
        
        return form_analysis
    
    async def test_navigation_elements(self, page):
        """Test navigation and interactive elements"""
        print("🧭 Testing Navigation Elements...")
        
        nav_analysis = await page.evaluate("""
            () => {
                const analysis = {
                    links: [],
                    navigation: [],
                    interactive: []
                };
                
                // Analyze links
                const links = document.querySelectorAll('a');
                links.forEach((link, index) => {
                    const linkRect = link.getBoundingClientRect();
                    const linkStyle = window.getComputedStyle(link);
                    
                    analysis.links.push({
                        index: index,
                        href: link.href,
                        text: link.textContent.trim(),
                        target: link.target,
                        className: link.className,
                        id: link.id,
                        dimensions: {
                            width: linkRect.width,
                            height: linkRect.height,
                            top: linkRect.top,
                            left: linkRect.left
                        },
                        style: {
                            display: linkStyle.display,
                            position: linkStyle.position,
                            padding: linkStyle.padding,
                            margin: linkStyle.margin,
                            backgroundColor: linkStyle.backgroundColor,
                            color: linkStyle.color,
                            textDecoration: linkStyle.textDecoration,
                            cursor: linkStyle.cursor
                        }
                    });
                });
                
                // Analyze navigation elements
                const navSelectors = ['nav', '.nav', '.navigation', '[class*="nav"]'];
                navSelectors.forEach(selector => {
                    const navElements = document.querySelectorAll(selector);
                    navElements.forEach((nav, index) => {
                        const navRect = nav.getBoundingClientRect();
                        const navStyle = window.getComputedStyle(nav);
                        
                        analysis.navigation.push({
                            selector: selector,
                            index: index,
                            id: nav.id,
                            className: nav.className,
                            dimensions: {
                                width: navRect.width,
                                height: navRect.height,
                                top: navRect.top,
                                left: navRect.left
                            },
                            style: {
                                display: navStyle.display,
                                position: navStyle.position,
                                flexDirection: navStyle.flexDirection,
                                justifyContent: navStyle.justifyContent,
                                alignItems: navStyle.alignItems,
                                backgroundColor: navStyle.backgroundColor
                            }
                        });
                    });
                });
                
                return analysis;
            }
        """)
        
        return nav_analysis
    
    async def generate_detailed_report(self, results):
        """Generate detailed test report"""
        print("📊 Generating Detailed Test Report...")
        
        report = {
            'test_summary': {
                'pages_tested': len(results),
                'test_types': ['Precise Measurements', 'Responsive Breakpoints', 'Form Elements', 'Navigation'],
                'timestamp': '2025-12-02 00:23:48'
            },
            'detailed_results': results,
            'pixel_issues': [],
            'responsive_issues': [],
            'ui_issues': [],
            'recommendations': []
        }
        
        # Analyze results for issues
        for page_name, page_results in results.items():
            if 'responsive_breakpoints' in page_results:
                for breakpoint_result in page_results['responsive_breakpoints']:
                    if breakpoint_result['is_problematic']:
                        report['responsive_issues'].append({
                            'page': page_name,
                            'breakpoint': breakpoint_result['breakpoint'],
                            'issues': breakpoint_result['issues']
                        })
            
            if 'precise_measurements' in page_results:
                measurements = page_results['precise_measurements']
                if measurements['responsiveIssues']['hasHorizontalScroll']:
                    report['pixel_issues'].append({
                        'page': page_name,
                        'issue': 'Horizontal scroll detected',
                        'scroll_width': measurements['body']['scrollWidth'],
                        'client_width': measurements['body']['clientWidth'],
                        'overflow': measurements['body']['scrollWidth'] - measurements['body']['clientWidth']
                    })
        
        # Generate recommendations
        report['recommendations'] = self._generate_detailed_recommendations(report)
        
        return report
    
    async def _generate_html_report(self, report):
        """Generate detailed HTML report"""
        html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>eTax Mobile PWA - Detailed UI Test Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #C60000 0%, #FF4444 100%);
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(45deg, #C60000, #FF4444);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .section {{
            padding: 30px;
            border-bottom: 1px solid #dee2e6;
        }}
        .section:last-child {{ border-bottom: none; }}
        .metric {{ 
            display: inline-block;
            background: #f8f9fa;
            padding: 10px 15px;
            margin: 5px;
            border-radius: 6px;
            border-left: 4px solid #C60000;
        }}
        .issue {{ 
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
        }}
        .critical {{ 
            background: #f8d7da;
            border-color: #f5c6cb;
        }}
        .recommendation {{
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
        }}
        .pixel-perfect {{
            background: #d4edda;
            border-color: #c3e6cb;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        th {{
            background: #f8f9fa;
            font-weight: bold;
        }}
        .breakpoint-pass {{ color: #28a745; }}
        .breakpoint-fail {{ color: #dc3545; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 eTax Mobile PWA - Detailed UI Test Report</h1>
            <p>Precise Pixel Measurements & Responsive Analysis</p>
            <p>Generated: {report['test_summary']['timestamp']}</p>
        </div>
        """
        
        # Add summary section
        html += f"""
        <div class="section">
            <h2>📊 Test Summary</h2>
            <div class="metric">Pages Tested: {report['test_summary']['pages_tested']}</div>
            <div class="metric">Responsive Issues: {len(report['responsive_issues'])}</div>
            <div class="metric">Pixel Issues: {len(report['pixel_issues'])}</div>
            <div class="metric">UI Issues: {len(report['ui_issues'])}</div>
        </div>
        """
        
        # Add responsive issues section
        if report['responsive_issues']:
            html += """
            <div class="section">
                <h2>⚠️ Responsive Issues Detected</h2>
            """
            for issue in report['responsive_issues']:
                html += f"""
                <div class="issue critical">
                    <h3>{issue['page']} - {issue['breakpoint']}</h3>
                    <ul>
                """
                for problem in issue['issues']:
                    html += f"<li>{problem}</li>"
                html += """
                    </ul>
                </div>
                """
            html += "</div>"
        
        # Add pixel issues section
        if report['pixel_issues']:
            html += """
            <div class="section">
                <h2>📏 Pixel Overflow Issues</h2>
            """
            for issue in report['pixel_issues']:
                html += f"""
                <div class="issue">
                    <h3>{issue['page']}</h3>
                    <p>Scroll Width: {issue['scroll_width']}px</p>
                    <p>Client Width: {issue['client_width']}px</p>
                    <p>Overflow: <strong>{issue['overflow']}px</strong></p>
                </div>
                """
            html += "</div>"
        
        # Add detailed results for each page
        html += '<div class="section"><h2>📄 Detailed Page Analysis</h2>'
        
        for page_name, page_results in report['detailed_results'].items():
            if 'error' not in page_results:
                html += f"""
                <h3>{page_name.upper()}</h3>
                <div class="pixel-perfect">
                    <h4>✅ Measurements</h4>
                """
                if 'precise_measurements' in page_results:
                    measurements = page_results['precise_measurements']
                    html += f"""
                    <p>Viewport: {measurements['viewport']['width']}x{measurements['viewport']['height']}</p>
                    <p>Document: {measurements['document']['width']}x{measurements['document']['height']}</p>
                    <p>Body: {measurements['body']['width']}x{measurements['body']['height']}</p>
                    """
                
                if 'responsive_breakpoints' in page_results:
                    html += "<h4>📱 Responsive Breakpoints</h4><table><tr><th>Breakpoint</th><th>Status</th><th>Issues</th></tr>"
                    for bp in page_results['responsive_breakpoints']:
                        status_class = "breakpoint-pass" if not bp['is_problematic'] else "breakpoint-fail"
                        status_text = "✅ PASS" if not bp['is_problematic'] else "❌ FAIL"
                        issues_text = ", ".join(bp['issues']) if bp['issues'] else "None"
                        html += f"""
                        <tr>
                            <td>{bp['breakpoint']}</td>
                            <td class="{status_class}">{status_text}</td>
                            <td>{issues_text}</td>
                        </tr>
                        """
                    html += "</table>"
                
                html += "</div>"
            else:
                html += f"""
                <div class="issue critical">
                    <h3>{page_name.upper()}</h3>
                    <p>Error: {page_results['error']}</p>
                </div>
                """
        
        html += "</div>"
        
        # Add recommendations
        html += '<div class="section"><h2>🎯 Recommendations</h2>'
        for rec in report['recommendations']:
            if rec.startswith('🔧') or rec.startswith('📏'):
                html += f'<div class="issue"><h4>{rec}</h4></div>'
            elif rec.startswith('🎯'):
                html += f'<div class="recommendation"><h4>{rec}</h4><ul>'
                continue
            else:
                html += f'<p>{rec}</p>'
        html += "</div>"
        
        html += """
    </div>
</body>
</html>
        """
        
        return html
    
    def _generate_detailed_recommendations(self, report):
        """Generate detailed recommendations based on issues found"""
        recommendations = []
        
        # Analyze responsive issues
        if report['responsive_issues']:
            recommendations.append("🔧 **Responsive Issues Found:**")
            for issue in report['responsive_issues']:
                recommendations.append(f"  - {issue['page']} at {issue['breakpoint']}: {', '.join(issue['issues'])}")
        
        # Analyze pixel issues
        if report['pixel_issues']:
            recommendations.append("📏 **Pixel Overflow Issues:**")
            for issue in report['pixel_issues']:
                overflow_pixels = issue['overflow']
                recommendations.append(f"  - {issue['page']}: {overflow_pixels}px horizontal overflow")
        
        # General UI recommendations
        recommendations.extend([
            "",
            "🎯 **General UI Improvements:**",
            "- Review CSS flexbox/grid layouts for responsive behavior",
            "- Implement proper media queries for all breakpoints",
            "- Test on actual mobile devices for final validation",
            "- Consider using CSS container queries for better component responsiveness",
            "- Add touch-friendly sizing for interactive elements (minimum 44px)"
        ])
        
        return recommendations

async def run_comprehensive_ui_test():
    """Run comprehensive UI test with detailed analysis"""
    tester = DetailedUITester()
    
    print("🚀 COMPREHENSIVE UI TESTING FOR ETAX MOBILE PWA")
    print("=" * 80)
    print("📏 FOCUS: Precise Pixel Measurements & Responsive Analysis")
    print("=" * 80)
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)  # Use headless mode
        
        # Test pages
        pages_to_test = [
            ("login", "file:///workspace/webapp/login.html"),
            ("home", "file:///workspace/webapp/home.html"),
            ("bien-lai", "file:///workspace/webapp/pages/bien-lai-dien-tu.html"),
            ("hoa-don", "file:///workspace/webapp/pages/hoa-don-dien-tu.html")
        ]
        
        results = {}
        
        for page_name, page_url in pages_to_test:
            print(f"\n🔍 TESTING: {page_name.upper()}")
            print("-" * 50)
            
            context = await browser.new_context(
                viewport={"width": 375, "height": 667, "isMobile": True}
            )
            page = await context.new_page()
            
            try:
                # Navigate to page
                print(f"📄 Loading {page_name} page...")
                await page.goto(page_url, wait_until="networkidle")
                await page.wait_for_timeout(2000)
                
                print(f"✅ {page_name} loaded successfully")
                
                # Run all tests
                page_results = {}
                
                # 1. Precise measurements
                print(f"📏 Testing precise measurements...")
                page_results['precise_measurements'] = await tester.test_precise_measurements(page)
                
                # 2. Responsive breakpoints
                print(f"📱 Testing responsive breakpoints...")
                page_results['responsive_breakpoints'] = await tester.test_responsive_breakpoints_detailed(page)
                
                # 3. Form elements (only for login page)
                if page_name == "login":
                    print(f"📝 Testing form elements...")
                    page_results['form_elements'] = await tester.test_form_elements_detailed(page)
                
                # 4. Navigation elements (only for home page)
                if page_name == "home":
                    print(f"🧭 Testing navigation elements...")
                    page_results['navigation_elements'] = await tester.test_navigation_elements(page)
                
                # Take screenshot
                screenshot_path = f"/workspace/test-results/detailed/{page_name}_detailed.png"
                Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
                await page.screenshot(path=screenshot_path, full_page=True)
                page_results['screenshot'] = screenshot_path
                
                results[page_name] = page_results
                print(f"✅ {page_name} testing completed")
                
            except Exception as e:
                print(f"❌ {page_name} testing failed: {str(e)}")
                results[page_name] = {'error': str(e)}
            
            await page.close()
            await context.close()
        
        await browser.close()
        
        # Generate detailed report
        print(f"\n📊 Generating detailed test report...")
        detailed_report = await tester.generate_detailed_report(results)
        
        # Save results
        results_path = Path("/workspace/test-results/detailed/detailed-ui-test-results.json")
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(detailed_report, f, indent=2, ensure_ascii=False)
        
        # Generate HTML report
        html_report = await tester._generate_html_report(detailed_report)
        html_path = Path("/workspace/test-results/detailed/detailed-ui-test-report.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"\n🎉 COMPREHENSIVE UI TESTING COMPLETED!")
        print(f"📊 Results: {results_path}")
        print(f"🌐 Report: {html_path}")
        print(f"📸 Screenshots: /workspace/test-results/detailed/")
        
        return detailed_report

async def main():
    """Main function"""
    await run_comprehensive_ui_test()

if __name__ == "__main__":
    asyncio.run(main())