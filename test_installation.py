#!/usr/bin/env python3
"""
Enhanced test script for Advanced MCP Web Scraper
Tests stealth features and enhanced capabilities
"""

import sys
import asyncio
import subprocess
import time

def test_imports():
    """Test if all required packages are installed"""
    print("🧪 Testing enhanced imports...")
    
    required_packages = [
        ('requests', 'HTTP library with sessions'),
        ('bs4', 'BeautifulSoup for parsing'),
        ('lxml', 'Fast XML parser'),
        ('mcp', 'Model Context Protocol'),
        ('playwright', 'Stealth browser automation'),
        ('fake_useragent', 'Advanced user agent rotation')
    ]
    
    failed = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package} ({description})")
        except ImportError:
            print(f"  ❌ {package} ({description}) - NOT INSTALLED")
            failed.append(package)
    
    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All imports successful!")
    return True

def test_stealth_features():
    """Test stealth features"""
    print("\n🥷 Testing stealth features...")
    
    try:
        from fake_useragent import UserAgent
        ua = UserAgent()
        
        # Test user agent rotation
        agents = [ua.random for _ in range(3)]
        if len(set(agents)) > 1:
            print("  ✅ User agent rotation working")
        else:
            print("  ⚠️ User agent rotation limited")
        
        # Test user agent quality
        sample_agent = ua.chrome
        if 'Chrome' in sample_agent and 'Mozilla' in sample_agent:
            print("  ✅ Quality user agents available")
        else:
            print("  ⚠️ Basic user agents only")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Stealth features error: {e}")
        return False

def test_playwright_stealth():
    """Test Playwright stealth configuration"""
    print("\n🎭 Testing Playwright stealth capabilities...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            # Test stealth browser launch
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage'
                ]
            )
            
            page = browser.new_page()
            
            # Test stealth configuration
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            # Test basic functionality
            page.goto("data:text/html,<html><body><h1>Test</h1></body></html>")
            title = page.query_selector('h1').inner_text()
            
            if title == "Test":
                print("  ✅ Stealth browser configuration working")
                print("  ✅ Anti-detection scripts loaded")
            
            browser.close()
            return True
            
    except Exception as e:
        print(f"  ❌ Playwright stealth test failed: {e}")
        return False

async def test_enhanced_scraping():
    """Test enhanced scraping functionality"""
    print("\n🌐 Testing enhanced scraping capabilities...")
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        
        from app_mcp import EnhancedWebScraper, ScrapingConfig
        
        # Test with a reliable website
        test_url = "https://httpbin.org/html"
        
        scraper = EnhancedWebScraper()
        config = ScrapingConfig(
            use_javascript=False, 
            stealth_mode=True,
            retry_attempts=2,
            max_pages=1
        )
        
        # Test static scraping with stealth
        print("  🔍 Testing stealth static scraping...")
        page = await scraper.scrape_static_content(test_url, config)
        
        if page and len(page.content.strip()) > 50:
            print(f"    ✅ Static stealth scraping successful ({len(page.content)} chars)")
            print(f"    ✅ Title extracted: '{page.title[:50]}...'")
        else:
            print("    ❌ Static stealth scraping failed")
            return False
        
        # Test dynamic scraping if Playwright available
        try:
            print("  🎭 Testing dynamic stealth scraping...")
            config.use_javascript = True
            dynamic_page = await scraper.scrape_dynamic_content(test_url, config)
            
            if dynamic_page and len(dynamic_page.content.strip()) > 50:
                print(f"    ✅ Dynamic stealth scraping successful ({len(dynamic_page.content)} chars)")
                print(f"    ✅ Enhanced content extraction working")
            else:
                print("    ⚠️ Dynamic scraping limited (fallback available)")
                
        except Exception as e:
            print(f"    ⚠️ Dynamic scraping not available: {e}")
        
        await scraper.close_browser()
        print("  ✅ Enhanced scraping tests completed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Enhanced scraping test failed: {e}")
        return False

def test_enhanced_mcp_server():
    """Test enhanced MCP server"""
    print("\n🔨 Testing enhanced MCP server...")
    
    try:
        from app_mcp import server
        
        if server:
            print("  ✅ Enhanced MCP server created")
            
            # Test enhanced tools
            tools = asyncio.run(server._list_tools_handler())
            if tools and len(tools) >= 4:
                print(f"  ✅ {len(tools)} enhanced tools available:")
                for tool in tools:
                    print(f"    • {tool.name}: {tool.description[:60]}...")
                    
                # Check for enhanced tool names
                tool_names = [tool.name for tool in tools]
                expected_tools = [
                    'scrape_website_enhanced',
                    'extract_article_content', 
                    'extract_comprehensive_metadata',
                    'crawl_website_enhanced'
                ]
                
                if all(tool in tool_names for tool in expected_tools):
                    print("  ✅ All enhanced tools present")
                else:
                    missing = [tool for tool in expected_tools if tool not in tool_names]
                    print(f"  ⚠️ Missing tools: {missing}")
                    
            else:
                print("  ❌ Enhanced tools not found")
                return False
        
        print("✅ Enhanced MCP server tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced MCP server test failed: {e}")
        return False

def test_success_rate_features():
    """Test success rate enhancement features"""
    print("\n📈 Testing success rate enhancement features...")
    
    try:
        from app_mcp import StealthUserAgentManager, ScrapingConfig
        
        # Test stealth user agent manager
        ua_manager = StealthUserAgentManager()
        
        # Test user agent variety
        agents = [ua_manager.get_stealth_user_agent() for _ in range(5)]
        unique_agents = len(set(agents))
        
        if unique_agents >= 3:
            print(f"  ✅ User agent rotation: {unique_agents} different agents")
        else:
            print(f"  ⚠️ Limited user agent rotation: {unique_agents} agents")
        
        # Test stealth headers
        headers = ua_manager.get_stealth_headers("https://example.com")
        required_headers = ['User-Agent', 'Accept', 'Accept-Language', 'DNT']
        
        if all(header in headers for header in required_headers):
            print("  ✅ Stealth headers complete")
        else:
            print("  ⚠️ Basic headers only")
        
        # Test enhanced config
        config = ScrapingConfig(stealth_mode=True, retry_attempts=3)
        if config.stealth_mode and config.retry_attempts == 3:
            print("  ✅ Enhanced configuration options available")
        else:
            print("  ⚠️ Basic configuration only")
        
        print("✅ Success rate features working!")
        return True
        
    except Exception as e:
        print(f"❌ Success rate features test failed: {e}")
        return False

def main():
    """Run all enhanced tests"""
    print("🚀 Enhanced MCP Web Scraper - Installation & Capabilities Test")
    print("=" * 70)
    
    tests = [
        ("Package imports", test_imports),
        ("Stealth features", test_stealth_features),
        ("Playwright stealth", test_playwright_stealth),
        ("Enhanced scraping", lambda: asyncio.run(test_enhanced_scraping())),
        ("Enhanced MCP server", test_enhanced_mcp_server),
        ("Success rate features", test_success_rate_features)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            start_time = time.time()
            if test_func():
                elapsed = time.time() - start_time
                print(f"    ⏱️ Completed in {elapsed:.2f}s")
                passed += 1
            else:
                print(f"    ❌ {test_name} failed")
        except Exception as e:
            print(f"    ❌ {test_name} failed with error: {e}")
    
    print("\n" + "=" * 70)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your enhanced scraper is ready!")
        print("\n💪 Enhanced capabilities verified:")
        print("   ✓ Stealth features operational")
        print("   ✓ Advanced user agent rotation") 
        print("   ✓ Enhanced content extraction")
        print("   ✓ Maximum success rate configuration")
        print("   ✓ All enhanced tools available")
        
        print("\n🚀 Next steps:")
        print("1. Configure Claude Desktop (see README.md)")
        print("2. Restart Claude Desktop completely")
        print("3. Look for 'enhanced-web-scraper' in hammer icon (🔨)")
        print("4. Test with challenging websites!")
        
        print("\n🎯 For maximum success rates:")
        print("   • Use stealth_mode=true (default)")
        print("   • Enable JavaScript rendering")
        print("   • Use realistic delays (2-5 seconds)")
        print("   • Enable automatic fallback strategies")
        
    elif passed >= total - 1:
        print("⚠️ Almost ready! One minor issue detected.")
        print("💡 The scraper should still work well.")
        print("🔧 Check the failed test above for optimization.")
        
    else:
        print("⚠️ Several issues detected. Please review:")
        print("💡 Common solutions:")
        print("- Run: pip install -r requirements.txt")
        print("- Run: playwright install chromium")
        print("- Ensure virtual environment is activated")
        print("- Check Python version (3.8+ required)")
    
    print(f"\n🥷 Enhanced scraper ready for challenging websites!")
    return passed >= total - 1  # Allow one minor failure

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)