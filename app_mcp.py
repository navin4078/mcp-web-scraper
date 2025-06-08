# Enhanced MCP Web Scraper with Improved Detection Resistance
# Focuses on legitimate techniques for better content extraction

import asyncio
import logging
import re
import time
import random
import json
import base64
from typing import Dict, List, Any, Optional, Set
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
import hashlib

# Core scraping libraries
import requests
from bs4 import BeautifulSoup, Comment
from fake_useragent import UserAgent

# Playwright for dynamic content scraping
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError

# MCP libraries
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ScrapingConfig:
    """Enhanced scraping configuration for better success rates"""
    max_pages: int = 10
    timeout: int = 45
    delay_range: tuple = (2, 5)  # Longer delays to appear more human
    use_javascript: bool = True
    user_agent_rotation: bool = True
    extract_metadata: bool = True
    extract_links: bool = True
    max_depth: int = 2
    wait_for_content: int = 5000  # Longer wait for JS content
    stealth_mode: bool = True  # Enhanced stealth features
    retry_attempts: int = 3
    use_proxy_rotation: bool = False  # Can be enabled if user has proxies
    respect_robots: bool = False  # Always ignore robots.txt for maximum access
    ignore_robots_txt: bool = True  # Explicitly skip robots.txt checking
    
class StealthUserAgentManager:
    """Advanced stealth user agent management"""
    
    def __init__(self):
        self.ua = UserAgent()
        # Real browser user agents updated regularly
        self.premium_agents = [
            # Chrome on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Chrome on Mac
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Firefox on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            # Firefox on Mac
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
            # Safari on Mac
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
            # Edge on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
        ]
        
    def get_stealth_user_agent(self) -> str:
        """Get a stealthy, realistic user agent"""
        return random.choice(self.premium_agents)
    
    def get_stealth_headers(self, url: str = None) -> Dict[str, str]:
        """Generate realistic, stealth headers"""
        headers = {
            'User-Agent': self.get_stealth_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Not A(Brand)";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Cache-Control': 'max-age=0',
        }
        
        # Add referer for internal navigation
        if url:
            parsed = urlparse(url)
            if parsed.netloc:
                headers['Referer'] = f"{parsed.scheme}://{parsed.netloc}/"
        
        return headers

@dataclass 
class ScrapedPage:
    """Enhanced scraped page data structure"""
    url: str
    title: str = ""
    content: str = ""
    metadata: Dict = None
    links: List[str] = None
    images: List[Dict] = None
    scrape_time: float = 0
    status_code: int = 0
    is_dynamic: bool = False
    depth: int = 0
    content_type: str = ""
    final_url: str = ""  # After redirects
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.links is None:
            self.links = []
        if self.images is None:
            self.images = []

class EnhancedWebScraper:
    """Enhanced web scraper with improved stealth and reliability"""
    
    def __init__(self):
        self.ua_manager = StealthUserAgentManager()
        self.scraped_pages: List[ScrapedPage] = []
        self.failed_urls: Set[str] = set()
        self.browser: Optional[Browser] = None
        self.playwright = None
        self.session = None  # Persistent session for cookies
        
    async def init_browser(self, config: ScrapingConfig):
        """Initialize stealth Playwright browser"""
        if config.use_javascript and not self.browser:
            self.playwright = await async_playwright().start()
            
            # Enhanced stealth browser setup
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-networking',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--disable-field-trial-config',
                    '--disable-ipc-flooding-protection',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--no-pings',
                    '--password-store=basic',
                    '--use-mock-keychain',
                    '--disable-component-extensions-with-background-pages',
                    '--disable-default-apps',
                    '--mute-audio',
                    '--no-zygote',
                    '--disable-client-side-phishing-detection',
                    '--disable-hang-monitor',
                    '--disable-popup-blocking',
                    '--disable-prompt-on-repost',
                    '--disable-sync',
                    '--disable-web-resources',
                    '--enable-automation',
                    '--log-level=3',
                    '--silent'
                ]
            )
            logger.info("🥷 Stealth browser initialized")
    
    async def create_stealth_page(self) -> Page:
        """Create a stealth-configured page"""
        page = await self.browser.new_page()
        
        # Remove automation detection
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            const originalQuery = window.navigator.permissions.query;
            return window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Remove chrome detection
            delete window.chrome;
        """)
        
        # Set realistic viewport
        await page.set_viewport_size({"width": 1366, "height": 768})
        
        # Set stealth user agent
        await page.set_user_agent(self.ua_manager.get_stealth_user_agent())
        
        return page
    
    async def close_browser(self):
        """Clean up browser resources"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        if self.session:
            self.session.close()
    
    async def scrape_static_content(self, url: str, config: ScrapingConfig) -> Optional[ScrapedPage]:
        """Enhanced static content scraping with stealth features"""
        start_time = time.time()
        
        try:
            if not self.session:
                self.session = requests.Session()
            
            headers = self.ua_manager.get_stealth_headers(url)
            
            # Multiple attempts with different strategies
            for attempt in range(config.retry_attempts):
                try:
                    # Add realistic delay
                    if attempt > 0:
                        delay = random.uniform(2, 5)
                        await asyncio.sleep(delay)
                    
                    response = self.session.get(
                        url, 
                        headers=headers, 
                        timeout=config.timeout,
                        allow_redirects=True,
                        verify=True
                    )
                    
                    # Check if we got blocked
                    if response.status_code == 403:
                        logger.warning(f"⚠️ 403 Forbidden on attempt {attempt + 1} for {url}")
                        if attempt < config.retry_attempts - 1:
                            continue
                    
                    if response.status_code == 429:
                        logger.warning(f"⚠️ Rate limited on attempt {attempt + 1} for {url}")
                        if attempt < config.retry_attempts - 1:
                            await asyncio.sleep(random.uniform(10, 20))
                            continue
                    
                    response.raise_for_status()
                    
                    # Check content type
                    content_type = response.headers.get('content-type', '').lower()
                    if 'text/html' not in content_type and 'application/xhtml' not in content_type:
                        logger.info(f"⏭️ Skipping non-HTML content: {url}")
                        return None
                    
                    soup = BeautifulSoup(response.content, 'lxml')
                    
                    page = ScrapedPage(
                        url=url,
                        final_url=response.url,
                        status_code=response.status_code,
                        content_type=content_type,
                        is_dynamic=False,
                        scrape_time=time.time() - start_time
                    )
                    
                    # Extract title
                    title_tag = soup.find('title')
                    page.title = title_tag.get_text().strip() if title_tag else ""
                    
                    # Enhanced content extraction
                    page.content = self._advanced_content_cleaning(soup)
                    
                    # Extract metadata
                    if config.extract_metadata:
                        page.metadata = self._extract_comprehensive_metadata(soup, response.headers)
                    
                    # Extract links
                    if config.extract_links:
                        page.links = self._extract_links(soup, response.url)
                    
                    # Extract images
                    page.images = self._extract_images(soup, response.url)
                    
                    if len(page.content.strip()) < 100:
                        logger.warning(f"⚠️ Very little content extracted from {url}, may be blocked")
                    else:
                        logger.info(f"✅ Static scraping: {url} ({len(page.content)} chars)")
                    
                    return page
                    
                except requests.exceptions.Timeout:
                    logger.warning(f"⏰ Timeout on attempt {attempt + 1} for {url}")
                    continue
                except requests.exceptions.ConnectionError:
                    logger.warning(f"🔌 Connection error on attempt {attempt + 1} for {url}")
                    continue
                except Exception as e:
                    logger.warning(f"⚠️ Error on attempt {attempt + 1} for {url}: {e}")
                    continue
            
            logger.error(f"❌ All static scraping attempts failed for {url}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Critical static scraping error for {url}: {e}")
            return None
    
    async def scrape_dynamic_content(self, url: str, config: ScrapingConfig) -> Optional[ScrapedPage]:
        """Enhanced dynamic content scraping with stealth features"""
        start_time = time.time()
        
        try:
            if not self.browser:
                await self.init_browser(config)
            
            page = await self.create_stealth_page()
            
            try:
                # Block unnecessary resources for speed and stealth
                await page.route("**/*", lambda route: (
                    route.abort() if route.request.resource_type in ['image', 'stylesheet', 'font', 'media']
                    else route.continue_()
                ))
                
                # Navigate with realistic behavior
                await page.goto(
                    url, 
                    wait_until='domcontentloaded',
                    timeout=config.timeout * 1000
                )
                
                # Human-like behavior simulation
                await asyncio.sleep(random.uniform(1, 3))
                
                # Scroll to trigger lazy loading
                await page.evaluate("""
                    async () => {
                        await new Promise(resolve => {
                            let totalHeight = 0;
                            const distance = 100;
                            const timer = setInterval(() => {
                                const scrollHeight = document.body.scrollHeight;
                                window.scrollBy(0, distance);
                                totalHeight += distance;
                                
                                if(totalHeight >= scrollHeight){
                                    clearInterval(timer);
                                    resolve();
                                }
                            }, 100);
                        });
                    }
                """)
                
                # Wait for content to load
                await page.wait_for_timeout(config.wait_for_content)
                
                # Wait for network to be idle
                try:
                    await page.wait_for_load_state('networkidle', timeout=10000)
                except:
                    pass  # Continue if network idle timeout
                
                # Get final content
                content = await page.content()
                soup = BeautifulSoup(content, 'lxml')
                
                scraped_page = ScrapedPage(
                    url=url,
                    final_url=page.url,
                    status_code=200,
                    is_dynamic=True,
                    scrape_time=time.time() - start_time
                )
                
                # Extract title
                scraped_page.title = await page.title()
                
                # Enhanced content extraction
                scraped_page.content = self._advanced_content_cleaning(soup)
                
                # Extract metadata
                if config.extract_metadata:
                    scraped_page.metadata = await self._extract_dynamic_metadata(page, soup)
                
                # Extract links
                if config.extract_links:
                    scraped_page.links = self._extract_links(soup, page.url)
                
                # Extract images
                scraped_page.images = self._extract_images(soup, page.url)
                
                if len(scraped_page.content.strip()) < 100:
                    logger.warning(f"⚠️ Very little content extracted from {url}, may be blocked or require interaction")
                else:
                    logger.info(f"✅ Dynamic scraping: {url} ({len(scraped_page.content)} chars)")
                
                return scraped_page
                
            finally:
                await page.close()
                
        except PlaywrightTimeoutError:
            logger.error(f"⏰ Dynamic scraping timeout for {url}")
            return None
        except Exception as e:
            logger.error(f"❌ Dynamic scraping failed for {url}: {e}")
            return None
    
    def _advanced_content_cleaning(self, soup: BeautifulSoup) -> str:
        """Advanced content cleaning with multiple strategies"""
        # Remove unwanted elements
        unwanted_selectors = [
            'script', 'style', 'noscript', 'iframe', 'object', 'embed',
            'nav', 'header', 'footer', 'aside', 
            '.advertisement', '.ads', '.popup', '.modal', '.sidebar',
            '.navigation', '.nav', '.menu', '.social', '.share',
            '.comment', '.comments', '.related', '.recommended',
            '[class*="ad-"]', '[id*="ad-"]', '[class*="ads"]', '[id*="ads"]',
            '.cookie-banner', '.cookie-notice', '.gdpr'
        ]
        
        for selector in unwanted_selectors:
            for element in soup.select(selector):
                element.decompose()
        
        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
        
        # Priority content extraction
        content_strategies = [
            # Strategy 1: Article content
            ['article', 'main', '[role="main"]'],
            # Strategy 2: Content containers
            ['.content', '.main-content', '.post-content', '.entry-content', 
             '.article-content', '.story-content', '.text-content'],
            # Strategy 3: Content IDs
            ['#content', '#main-content', '#article', '#story'],
            # Strategy 4: Common news/blog patterns
            ['.post-body', '.entry', '.story', '.article-body'],
            # Strategy 5: Fallback to body
            ['body']
        ]
        
        main_content = ""
        for strategy in content_strategies:
            for selector in strategy:
                elements = soup.select(selector)
                if elements:
                    texts = []
                    for elem in elements:
                        text = elem.get_text()
                        if len(text.strip()) > 100:  # Only substantial content
                            texts.append(text)
                    
                    if texts:
                        main_content = ' '.join(texts)
                        break
            
            if main_content and len(main_content.strip()) > 200:
                break
        
        if not main_content:
            # Last resort: get all text
            main_content = soup.get_text()
        
        # Advanced text cleaning
        main_content = re.sub(r'\n\s*\n+', '\n\n', main_content)
        main_content = re.sub(r'[ \t]+', ' ', main_content)
        main_content = re.sub(r'\r\n?', '\n', main_content)
        
        # Remove very short lines and common UI text
        lines = main_content.split('\n')
        cleaned_lines = []
        skip_patterns = [
            r'^(home|about|contact|login|register|sign in|sign up|menu|search|subscribe)$',
            r'^(privacy|terms|cookies|gdpr|accept|decline|close|×)$',
            r'^[\d\s\-\.\(\)]+$',  # Numbers and symbols only
            r'^[^\w]*$'  # Non-word characters only
        ]
        
        for line in lines:
            line = line.strip()
            if len(line) > 20:  # Substantial content only
                skip = False
                for pattern in skip_patterns:
                    if re.match(pattern, line.lower()):
                        skip = True
                        break
                if not skip:
                    cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
    
    def _extract_comprehensive_metadata(self, soup: BeautifulSoup, headers: Dict) -> Dict:
        """Extract comprehensive metadata"""
        metadata = {
            'basic': {},
            'open_graph': {},
            'twitter': {},
            'schema_org': [],
            'technical': {}
        }
        
        # Basic meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            content = meta.get('content', '')
            if name and content:
                metadata['basic'][name] = content
        
        # Open Graph
        for meta in soup.find_all('meta', property=lambda x: x and x.startswith('og:')):
            property_name = meta.get('property', '')
            content = meta.get('content', '')
            if property_name and content:
                metadata['open_graph'][property_name] = content
        
        # Twitter Cards
        for meta in soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')}):
            name = meta.get('name', '')
            content = meta.get('content', '')
            if name and content:
                metadata['twitter'][name] = content
        
        # Schema.org structured data
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                metadata['schema_org'].append(data)
            except:
                pass
        
        # Technical metadata
        metadata['technical'] = {
            'content_type': headers.get('content-type', ''),
            'server': headers.get('server', ''),
            'last_modified': headers.get('last-modified', ''),
            'content_length': headers.get('content-length', ''),
            'encoding': headers.get('content-encoding', '')
        }
        
        return metadata
    
    async def _extract_dynamic_metadata(self, page: Page, soup: BeautifulSoup) -> Dict:
        """Extract metadata from dynamic page"""
        metadata = self._extract_comprehensive_metadata(soup, {})
        
        try:
            # Additional dynamic metadata
            js_metadata = await page.evaluate("""
                () => {
                    const meta = {};
                    
                    // Get all meta tags via JS
                    document.querySelectorAll('meta').forEach(tag => {
                        const name = tag.getAttribute('name') || tag.getAttribute('property');
                        const content = tag.getAttribute('content');
                        if (name && content) {
                            meta[name] = content;
                        }
                    });
                    
                    // Additional browser info
                    meta['_viewport'] = {
                        width: window.innerWidth,
                        height: window.innerHeight
                    };
                    
                    meta['_url'] = window.location.href;
                    meta['_title'] = document.title;
                    
                    return meta;
                }
            """)
            
            metadata['dynamic'] = js_metadata
            
        except Exception as e:
            logger.warning(f"Failed to extract dynamic metadata: {e}")
        
        return metadata
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Enhanced link extraction"""
        links = []
        base_domain = urlparse(base_url).netloc
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if not href:
                continue
            
            # Skip javascript and mail links
            if href.startswith(('javascript:', 'mailto:', 'tel:')):
                continue
            
            # Convert relative URLs to absolute
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            
            # Only include links from same domain
            if parsed.netloc == base_domain:
                # Clean URL
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if parsed.query and len(parsed.query) < 200:  # Include reasonable queries
                    clean_url += f"?{parsed.query}"
                
                # Skip unwanted file types
                skip_extensions = [
                    '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
                    '.mp4', '.mp3', '.avi', '.mov', '.zip', '.exe', '.dmg',
                    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
                ]
                
                if not any(clean_url.lower().endswith(ext) for ext in skip_extensions):
                    if '#' not in clean_url:  # Skip fragments
                        links.append(clean_url)
        
        return list(set(links))[:50]  # Deduplicate and limit
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Enhanced image extraction"""
        images = []
        
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src:
                full_url = urljoin(base_url, src)
                
                # Skip data URLs and very small images
                if not src.startswith('data:') and 'pixel' not in src.lower():
                    images.append({
                        'src': full_url,
                        'alt': img.get('alt', ''),
                        'title': img.get('title', ''),
                        'width': img.get('width', ''),
                        'height': img.get('height', ''),
                        'class': ' '.join(img.get('class', [])),
                        'loading': img.get('loading', '')
                    })
        
        return images[:30]  # Limit to 30 images
    
    async def crawl_website(self, start_url: str, config: ScrapingConfig) -> List[ScrapedPage]:
        """Enhanced website crawling with better success rates"""
        logger.info(f"🌐 Starting enhanced crawl: {start_url}")
        logger.info(f"📊 Config: {config.max_pages} pages, depth {config.max_depth}, stealth: {config.stealth_mode}")
        
        scraped_pages = []
        urls_to_process = [(start_url, 0)]
        processed_urls = set()
        
        try:
            if config.use_javascript:
                await self.init_browser(config)
            
            while urls_to_process and len(scraped_pages) < config.max_pages:
                current_url, depth = urls_to_process.pop(0)
                
                if current_url in processed_urls or depth > config.max_depth:
                    continue
                
                processed_urls.add(current_url)
                
                # Human-like delay
                if config.delay_range:
                    delay = random.uniform(*config.delay_range)
                    logger.info(f"⏱️ Waiting {delay:.1f}s before next request")
                    await asyncio.sleep(delay)
                
                # Try dynamic first, then static
                page = None
                if config.use_javascript:
                    page = await self.scrape_dynamic_content(current_url, config)
                
                if not page or len(page.content.strip()) < 100:
                    logger.info("🔄 Trying static scraping as fallback")
                    static_page = await self.scrape_static_content(current_url, config)
                    if static_page and len(static_page.content.strip()) > len(page.content.strip() if page else ""):
                        page = static_page
                
                if page and len(page.content.strip()) > 50:
                    page.depth = depth
                    scraped_pages.append(page)
                    
                    # Add discovered links for next depth
                    if depth < config.max_depth and page.links:
                        new_links = [link for link in page.links[:10] if link not in processed_urls]
                        for link in new_links:
                            urls_to_process.append((link, depth + 1))
                    
                    logger.info(f"📄 Success {len(scraped_pages)}/{config.max_pages}: {current_url} ({len(page.content)} chars)")
                else:
                    self.failed_urls.add(current_url)
                    logger.warning(f"❌ Failed to extract content from: {current_url}")
            
            success_rate = len(scraped_pages) / max(len(processed_urls), 1) * 100
            logger.info(f"✅ Crawling completed: {len(scraped_pages)} pages, {success_rate:.1f}% success rate")
            return scraped_pages
            
        finally:
            await self.close_browser()

# Create MCP server
server = Server("enhanced-web-scraper")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available enhanced web scraping tools"""
    return [
        Tool(
            name="scrape_website_enhanced",
            description="Enhanced web scraping with improved detection resistance and stealth features",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to scrape"
                    },
                    "extract_type": {
                        "type": "string", 
                        "enum": ["text", "links", "images", "metadata", "all"],
                        "description": "Type of data to extract",
                        "default": "text"
                    },
                    "use_javascript": {
                        "type": "boolean",
                        "description": "Enable JavaScript rendering for dynamic content",
                        "default": True
                    },
                    "max_pages": {
                        "type": "integer",
                        "description": "Maximum number of pages to scrape",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20
                    },
                    "crawl_depth": {
                        "type": "integer",
                        "description": "How deep to crawl (0=current page only, 1-2=include linked pages)",
                        "default": 0,
                        "minimum": 0,
                        "maximum": 2
                    },
                    "stealth_mode": {
                        "type": "boolean",
                        "description": "Enable enhanced stealth features for better success rates",
                        "default": True
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="extract_article_content",
            description="Extract main article content with advanced content detection",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to extract article content from"
                    },
                    "use_javascript": {
                        "type": "boolean",
                        "description": "Enable JavaScript rendering",
                        "default": True
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="extract_comprehensive_metadata",
            description="Extract all available metadata including Open Graph, Twitter Cards, and Schema.org",
            inputSchema={
                "type": "object", 
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to extract metadata from"
                    },
                    "include_technical": {
                        "type": "boolean",
                        "description": "Include technical metadata (headers, server info)",
                        "default": True
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="crawl_website_enhanced",
            description="Enhanced website crawling with improved success rates and stealth features",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string", 
                        "description": "The starting URL to crawl"
                    },
                    "max_pages": {
                        "type": "integer",
                        "description": "Maximum number of pages to crawl",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 30
                    },
                    "max_depth": {
                        "type": "integer",
                        "description": "Maximum crawling depth",
                        "default": 2,
                        "minimum": 1,
                        "maximum": 3
                    },
                    "content_focus": {
                        "type": "string",
                        "enum": ["articles", "products", "general"],
                        "description": "Focus crawling on specific content types",
                        "default": "general"
                    }
                },
                "required": ["url"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle enhanced tool calls"""
    
    if name == "scrape_website_enhanced":
        return await scrape_website_enhanced_tool(arguments)
    elif name == "extract_article_content":
        return await extract_article_content_tool(arguments)
    elif name == "extract_comprehensive_metadata":
        return await extract_comprehensive_metadata_tool(arguments)
    elif name == "crawl_website_enhanced":
        return await crawl_website_enhanced_tool(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def scrape_website_enhanced_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Enhanced website scraping with improved success rates"""
    try:
        url = args["url"]
        extract_type = args.get("extract_type", "text")
        use_javascript = args.get("use_javascript", True)
        max_pages = args.get("max_pages", 5)
        crawl_depth = args.get("crawl_depth", 0)
        stealth_mode = args.get("stealth_mode", True)
        
        logger.info(f"🔍 Enhanced scraping: {url} (JS: {use_javascript}, Stealth: {stealth_mode})")
        
        config = ScrapingConfig(
            max_pages=max_pages,
            max_depth=crawl_depth,
            use_javascript=use_javascript,
            stealth_mode=stealth_mode,
            delay_range=(2, 5),
            retry_attempts=3
        )
        
        scraper = EnhancedWebScraper()
        
        if crawl_depth > 0:
            pages = await scraper.crawl_website(url, config)
        else:
            # Single page scraping with fallback
            page = None
            if use_javascript:
                page = await scraper.scrape_dynamic_content(url, config)
            
            if not page or len(page.content.strip()) < 100:
                static_page = await scraper.scrape_static_content(url, config)
                if static_page and len(static_page.content.strip()) > len(page.content.strip() if page else ""):
                    page = static_page
            
            pages = [page] if page else []
        
        if not pages:
            return [TextContent(type="text", text=f"❌ Unable to extract content from {url}. The site may have strong anti-bot protection or the content may be behind authentication.")]
        
        # Format results
        result = {
            "url": url,
            "pages_scraped": len(pages),
            "extraction_type": extract_type,
            "success_indicators": {
                "content_extracted": sum(1 for p in pages if len(p.content.strip()) > 100),
                "dynamic_pages": sum(1 for p in pages if p.is_dynamic),
                "average_content_length": sum(len(p.content) for p in pages) // max(len(pages), 1)
            }
        }
        
        if extract_type in ["text", "all"]:
            result["content"] = []
            for page in pages:
                content_preview = page.content[:1500] + "..." if len(page.content) > 1500 else page.content
                result["content"].append({
                    "url": page.url,
                    "final_url": page.final_url,
                    "title": page.title,
                    "text": content_preview,
                    "full_length": len(page.content),
                    "word_count": len(page.content.split()),
                    "is_dynamic": page.is_dynamic,
                    "scrape_time": round(page.scrape_time, 2)
                })
        
        if extract_type in ["links", "all"]:
            all_links = []
            for page in pages:
                for link in page.links:
                    all_links.append({"url": link, "source_page": page.url})
            result["links"] = all_links[:100]
        
        if extract_type in ["images", "all"]:
            all_images = []
            for page in pages:
                for img in page.images:
                    img["source_page"] = page.url
                    all_images.append(img)
            result["images"] = all_images[:50]
        
        if extract_type in ["metadata", "all"]:
            result["metadata"] = []
            for page in pages:
                result["metadata"].append({
                    "url": page.url,
                    "title": page.title,
                    "metadata": page.metadata,
                    "is_dynamic": page.is_dynamic
                })
        
        return [TextContent(type="text", text=f"✅ Enhanced scraping completed for {url}\n\n{json.dumps(result, indent=2, ensure_ascii=False)}")]
        
    except Exception as e:
        logger.error(f"❌ Enhanced scraping error: {e}")
        return [TextContent(type="text", text=f"❌ Error during enhanced scraping: {str(e)}")]

async def extract_article_content_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Extract main article content with advanced detection"""
    try:
        url = args["url"]
        use_javascript = args.get("use_javascript", True)
        
        config = ScrapingConfig(use_javascript=use_javascript, stealth_mode=True)
        scraper = EnhancedWebScraper()
        
        # Try both methods and pick the best result
        dynamic_page = None
        static_page = None
        
        if use_javascript:
            dynamic_page = await scraper.scrape_dynamic_content(url, config)
        
        static_page = await scraper.scrape_static_content(url, config)
        
        # Choose the page with more substantial content
        page = None
        if dynamic_page and static_page:
            if len(dynamic_page.content.strip()) > len(static_page.content.strip()):
                page = dynamic_page
            else:
                page = static_page
        elif dynamic_page:
            page = dynamic_page
        elif static_page:
            page = static_page
        
        if not page or len(page.content.strip()) < 50:
            return [TextContent(type="text", text=f"❌ Unable to extract article content from {url}. The content may be behind a paywall, require authentication, or have strong anti-bot protection.")]
        
        # Extract article-specific information
        soup = BeautifulSoup(page.content, 'lxml') if not page.is_dynamic else BeautifulSoup(page.content, 'lxml')
        
        # Try to find article metadata
        article_info = {
            "url": url,
            "title": page.title,
            "content": page.content,
            "word_count": len(page.content.split()),
            "estimated_read_time": len(page.content.split()) // 200,  # Assume 200 WPM
            "extraction_method": "dynamic" if page.is_dynamic else "static",
            "content_indicators": {
                "has_substantial_content": len(page.content.strip()) > 200,
                "has_paragraphs": page.content.count('\n\n') > 2,
                "content_length": len(page.content),
                "may_be_truncated": "..." in page.content or len(page.content) > 10000
            }
        }
        
        # Try to extract author and date
        if page.metadata:
            basic_meta = page.metadata.get('basic', {})
            article_info.update({
                "author": basic_meta.get('author', ''),
                "published_date": basic_meta.get('date', ''),
                "description": basic_meta.get('description', '')
            })
        
        return [TextContent(type="text", text=f"📄 Article content extracted from {url}\n\n{json.dumps(article_info, indent=2, ensure_ascii=False)}")]
        
    except Exception as e:
        logger.error(f"❌ Article extraction error: {e}")
        return [TextContent(type="text", text=f"❌ Error extracting article content: {str(e)}")]

async def extract_comprehensive_metadata_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Extract comprehensive metadata"""
    try:
        url = args["url"]
        include_technical = args.get("include_technical", True)
        
        config = ScrapingConfig(use_javascript=True, extract_metadata=True, stealth_mode=True)
        scraper = EnhancedWebScraper()
        
        page = await scraper.scrape_dynamic_content(url, config)
        if not page:
            page = await scraper.scrape_static_content(url, config)
        
        if not page:
            return [TextContent(type="text", text=f"❌ Failed to extract metadata from {url}")]
        
        result = {
            "url": url,
            "final_url": page.final_url,
            "title": page.title,
            "metadata": page.metadata,
            "extraction_info": {
                "method": "dynamic" if page.is_dynamic else "static",
                "scrape_time": round(page.scrape_time, 2),
                "content_length": len(page.content),
                "status_code": page.status_code
            }
        }
        
        if not include_technical and 'technical' in result['metadata']:
            del result['metadata']['technical']
        
        return [TextContent(type="text", text=f"📊 Comprehensive metadata from {url}\n\n{json.dumps(result, indent=2, ensure_ascii=False)}")]
        
    except Exception as e:
        logger.error(f"❌ Metadata extraction error: {e}")
        return [TextContent(type="text", text=f"❌ Error extracting metadata: {str(e)}")]

async def crawl_website_enhanced_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Enhanced website crawling with improved success rates"""
    try:
        url = args["url"]
        max_pages = args.get("max_pages", 10)
        max_depth = args.get("max_depth", 2)
        content_focus = args.get("content_focus", "general")
        
        logger.info(f"🕷️ Enhanced crawling: {url} (pages: {max_pages}, depth: {max_depth})")
        
        config = ScrapingConfig(
            max_pages=max_pages,
            max_depth=max_depth,
            use_javascript=True,
            stealth_mode=True,
            delay_range=(3, 6),  # Longer delays for crawling
            retry_attempts=3
        )
        
        scraper = EnhancedWebScraper()
        pages = await scraper.crawl_website(url, config)
        
        if not pages:
            return [TextContent(type="text", text=f"❌ Unable to crawl {url}. The site may have strong anti-crawling protection.")]
        
        # Analyze crawl results
        result = {
            "crawl_summary": {
                "start_url": url,
                "pages_found": len(pages),
                "pages_requested": max_pages,
                "max_depth": max_depth,
                "success_rate": f"{len(pages) / max_pages * 100:.1f}%",
                "failed_urls": len(scraper.failed_urls),
                "content_focus": content_focus
            },
            "content_analysis": {
                "total_content_length": sum(len(p.content) for p in pages),
                "total_word_count": sum(len(p.content.split()) for p in pages),
                "average_content_per_page": sum(len(p.content) for p in pages) // max(len(pages), 1),
                "dynamic_pages_count": sum(1 for p in pages if p.is_dynamic),
                "pages_with_substantial_content": sum(1 for p in pages if len(p.content.strip()) > 500)
            },
            "page_details": [],
            "discovered_links": []
        }
        
        # Add page details
        for page in pages:
            page_info = {
                "url": page.url,
                "final_url": page.final_url,
                "title": page.title,
                "depth": page.depth,
                "content_length": len(page.content),
                "word_count": len(page.content.split()),
                "links_found": len(page.links),
                "images_found": len(page.images),
                "is_dynamic": page.is_dynamic,
                "scrape_time": round(page.scrape_time, 2),
                "content_preview": page.content[:300] + "..." if len(page.content) > 300 else page.content
            }
            result["page_details"].append(page_info)
        
        # Collect unique links
        all_links = set()
        for page in pages:
            all_links.update(page.links)
        result["discovered_links"] = list(all_links)[:100]
        
        return [TextContent(type="text", text=f"🕷️ Enhanced crawling completed for {url}\n\n{json.dumps(result, indent=2, ensure_ascii=False)}")]
        
    except Exception as e:
        logger.error(f"❌ Enhanced crawling error: {e}")
        return [TextContent(type="text", text=f"❌ Error during enhanced crawling: {str(e)}")]

async def main():
    """Main entry point"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    logger.info("🥷 Starting Enhanced MCP Web Scraper with Stealth Features")
    asyncio.run(main())