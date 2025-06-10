# Enhanced MCP Web Scraper with Advanced Stealth Features
# Improved scraper with better success rates and anti-detection measures

import asyncio
import logging
import random
import time
import json
from typing import Dict, List, Any, Optional, Union
from urllib.parse import urljoin, urlparse
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel
import chardet
import html

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
server = Server("enhanced-web-scraper")

class StealthConfig:
    """Configuration for stealth scraping features"""
    
    # Rotate between different realistic user agents
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    # Common browser headers to appear more legitimate
    BROWSER_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    }

class EnhancedScraper:
    """Enhanced web scraper with stealth features and resilience"""
    
    def __init__(self):
        self.session = requests.Session()
        self._setup_session()
        
    def _setup_session(self):
        """Configure session with retry strategy and realistic headers"""
        # Setup retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update(StealthConfig.BROWSER_HEADERS)
        
    def _get_stealth_headers(self, url: str) -> Dict[str, str]:
        """Generate stealth headers for the request"""
        headers = StealthConfig.BROWSER_HEADERS.copy()
        headers['User-Agent'] = random.choice(StealthConfig.USER_AGENTS)
        
        # Add referer for internal links
        parsed_url = urlparse(url)
        if parsed_url.netloc:
            headers['Referer'] = f"{parsed_url.scheme}://{parsed_url.netloc}/"
            
        return headers
    
    def _detect_encoding(self, response: requests.Response) -> str:
        """Detect proper encoding for the response"""
        # Try to get encoding from response headers
        if response.encoding and response.encoding.lower() != 'iso-8859-1':
            return response.encoding
            
        # Use chardet to detect encoding from content
        raw_data = response.content
        detected = chardet.detect(raw_data)
        if detected and detected['confidence'] > 0.7:
            return detected['encoding']
            
        # Fallback to UTF-8
        return 'utf-8'
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
            
        # Decode HTML entities
        text = html.unescape(text)
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def fetch_with_fallback(self, url: str, use_javascript: bool = False) -> BeautifulSoup:
        """
        Fetch webpage with multiple fallback strategies
        """
        errors = []
        
        # Strategy 1: Enhanced requests with stealth headers
        try:
            return self._fetch_with_requests(url)
        except Exception as e:
            errors.append(f"Requests method failed: {str(e)}")
            logger.warning(f"Requests method failed for {url}: {e}")
        
        # Strategy 2: Simplified requests with minimal headers
        try:
            return self._fetch_simple(url)
        except Exception as e:
            errors.append(f"Simple method failed: {str(e)}")
            logger.warning(f"Simple method failed for {url}: {e}")
            
        # Strategy 3: Raw content approach
        try:
            return self._fetch_raw(url)
        except Exception as e:
            errors.append(f"Raw method failed: {str(e)}")
            logger.warning(f"Raw method failed for {url}: {e}")
        
        # If all strategies fail, raise combined error
        raise Exception(f"All fetch strategies failed for {url}. Errors: {'; '.join(errors)}")
    
    def _fetch_with_requests(self, url: str) -> BeautifulSoup:
        """Primary fetch method with stealth features"""
        headers = self._get_stealth_headers(url)
        
        # Add random delay to appear more human-like
        time.sleep(random.uniform(0.5, 2.0))
        
        response = self.session.get(
            url, 
            headers=headers, 
            timeout=30,
            allow_redirects=True,
            verify=True
        )
        
        response.raise_for_status()
        
        # Detect and use proper encoding
        encoding = self._detect_encoding(response)
        response.encoding = encoding
        
        # Parse with multiple parsers as fallback
        try:
            return BeautifulSoup(response.text, 'lxml')
        except:
            try:
                return BeautifulSoup(response.text, 'html.parser')
            except:
                return BeautifulSoup(response.content, 'html.parser')
    
    def _fetch_simple(self, url: str) -> BeautifulSoup:
        """Simplified fetch method"""
        simple_headers = {
            'User-Agent': random.choice(StealthConfig.USER_AGENTS)
        }
        
        response = requests.get(url, headers=simple_headers, timeout=20)
        response.raise_for_status()
        
        # Auto-detect encoding
        encoding = self._detect_encoding(response)
        response.encoding = encoding
        
        return BeautifulSoup(response.text, 'html.parser')
    
    def _fetch_raw(self, url: str) -> BeautifulSoup:
        """Raw fetch method as last resort"""
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # Use raw content and let BeautifulSoup handle encoding
        return BeautifulSoup(response.content, 'html.parser')

# Global scraper instance
scraper = EnhancedScraper()

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools"""
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
                    "stealth_mode": {
                        "type": "boolean", 
                        "description": "Enable enhanced stealth features for better success rates",
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
    """Handle tool calls"""
    
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
    """Enhanced website scraping with stealth features"""
    try:
        url = args["url"]
        extract_type = args.get("extract_type", "text")
        use_javascript = args.get("use_javascript", True)
        stealth_mode = args.get("stealth_mode", True)
        max_pages = args.get("max_pages", 5)
        crawl_depth = args.get("crawl_depth", 0)
        
        logger.info(f"Scraping {url} with enhanced features")
        
        # Fetch and parse the webpage
        soup = scraper.fetch_with_fallback(url, use_javascript=use_javascript)
        
        # Extract title safely
        title = "No title found"
        if soup.title and soup.title.string:
            title = scraper._clean_text(soup.title.string)
        
        # Extract data based on type
        data = []
        
        if extract_type == "text" or extract_type == "all":
            # Extract text content with better filtering
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span'])
            for elem in text_elements[:50]:  # Limit to prevent overwhelming output
                text = scraper._clean_text(elem.get_text())
                if text and len(text) > 10:  # Filter out very short text
                    data.append({
                        'type': 'text',
                        'content': text,
                        'tag': elem.name,
                        'class': elem.get('class', []),
                        'id': elem.get('id', '')
                    })
        
        if extract_type == "links" or extract_type == "all":
            # Extract links with better URL handling
            links = soup.find_all('a', href=True)
            for link in links[:20]:  # Limit links
                href = link.get('href')
                if href:
                    # Convert relative URLs to absolute
                    absolute_url = urljoin(url, href)
                    link_text = scraper._clean_text(link.get_text())
                    if link_text:  # Only include links with text
                        data.append({
                            'type': 'link',
                            'url': absolute_url,
                            'text': link_text,
                            'title': link.get('title', ''),
                            'is_external': urlparse(absolute_url).netloc != urlparse(url).netloc
                        })
        
        if extract_type == "images" or extract_type == "all":
            # Extract images with better URL handling
            images = soup.find_all('img', src=True)
            for img in images[:15]:  # Limit images
                src = img.get('src')
                if src:
                    absolute_url = urljoin(url, src)
                    data.append({
                        'type': 'image',
                        'src': absolute_url,
                        'alt': scraper._clean_text(img.get('alt', '')),
                        'title': scraper._clean_text(img.get('title', '')),
                        'width': img.get('width'),
                        'height': img.get('height')
                    })
        
        if extract_type == "metadata" or extract_type == "all":
            # Extract comprehensive metadata
            metadata = extract_metadata(soup, url)
            data.append({
                'type': 'metadata',
                'content': metadata
            })
        
        result = {
            'url': url,
            'title': title,
            'extract_type': extract_type,
            'total_items': len(data),
            'success': True,
            'data': data,
            'timestamp': time.time(),
            'scraper_version': 'enhanced-v2.0'
        }
        
        return [TextContent(
            type="text", 
            text=f"✅ Successfully scraped {url}\n\n" + json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        error_msg = f"❌ Error scraping website: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=error_msg)]

async def extract_article_content_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Extract main article content"""
    try:
        url = args["url"]
        use_javascript = args.get("use_javascript", True)
        
        soup = scraper.fetch_with_fallback(url, use_javascript=use_javascript)
        
        # Try to find main content areas
        content_selectors = [
            'article', '[role="main"]', 'main', '.content', '#content',
            '.post-content', '.entry-content', '.article-content',
            '.story-body', '.article-body'
        ]
        
        main_content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                main_content = scraper._clean_text(elements[0].get_text())
                break
        
        # Fallback: extract paragraphs
        if not main_content:
            paragraphs = soup.find_all('p')
            main_content = '\n\n'.join([scraper._clean_text(p.get_text()) for p in paragraphs[:10] if p.get_text().strip()])
        
        title = scraper._clean_text(soup.title.string) if soup.title else "No title"
        
        result = {
            'url': url,
            'title': title,
            'content': main_content,
            'content_length': len(main_content),
            'extraction_method': 'enhanced_article_extraction'
        }
        
        return [TextContent(
            type="text",
            text=f"📰 Article content extracted from {url}\n\n" + json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error extracting article: {str(e)}")]

async def extract_comprehensive_metadata_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Extract comprehensive metadata"""
    try:
        url = args["url"]
        include_technical = args.get("include_technical", True)
        
        soup = scraper.fetch_with_fallback(url)
        metadata = extract_metadata(soup, url, include_technical)
        
        return [TextContent(
            type="text",
            text=f"🔍 Comprehensive metadata from {url}\n\n" + json.dumps(metadata, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error extracting metadata: {str(e)}")]

async def crawl_website_enhanced_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Enhanced website crawling"""
    try:
        start_url = args["url"]
        max_pages = args.get("max_pages", 10)
        max_depth = args.get("max_depth", 2)
        content_focus = args.get("content_focus", "general")
        
        crawled_pages = []
        to_crawl = [(start_url, 0)]  # (url, depth)
        visited = set()
        
        while to_crawl and len(crawled_pages) < max_pages:
            current_url, depth = to_crawl.pop(0)
            
            if current_url in visited or depth > max_depth:
                continue
                
            visited.add(current_url)
            
            try:
                soup = scraper.fetch_with_fallback(current_url)
                title = scraper._clean_text(soup.title.string) if soup.title else "No title"
                
                # Extract summary content
                paragraphs = soup.find_all('p')
                summary = ' '.join([scraper._clean_text(p.get_text()) for p in paragraphs[:3]])[:500]
                
                page_data = {
                    'url': current_url,
                    'title': title,
                    'summary': summary,
                    'depth': depth,
                    'timestamp': time.time()
                }
                
                crawled_pages.append(page_data)
                
                # Find links for next level crawling
                if depth < max_depth:
                    links = soup.find_all('a', href=True)
                    for link in links[:10]:  # Limit links per page
                        href = link.get('href')
                        if href:
                            absolute_url = urljoin(current_url, href)
                            # Only crawl same domain
                            if urlparse(absolute_url).netloc == urlparse(start_url).netloc:
                                to_crawl.append((absolute_url, depth + 1))
                
                # Add delay between requests
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.warning(f"Failed to crawl {current_url}: {e}")
                continue
        
        result = {
            'start_url': start_url,
            'total_pages_crawled': len(crawled_pages),
            'max_depth_reached': max([p['depth'] for p in crawled_pages]) if crawled_pages else 0,
            'pages': crawled_pages
        }
        
        return [TextContent(
            type="text",
            text=f"🕷️ Crawled {len(crawled_pages)} pages from {start_url}\n\n" + json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error crawling website: {str(e)}")]

def extract_metadata(soup: BeautifulSoup, url: str, include_technical: bool = True) -> Dict[str, Any]:
    """Extract comprehensive metadata from webpage"""
    metadata = {
        'url': url,
        'title': scraper._clean_text(soup.title.string) if soup.title else None,
        'description': None,
        'keywords': None,
        'author': None,
        'canonical_url': None,
        'open_graph': {},
        'twitter_cards': {},
        'schema_org': [],
        'meta_tags': {}
    }
    
    # Extract meta tags
    meta_tags = soup.find_all('meta')
    for tag in meta_tags:
        name = tag.get('name', '').lower()
        property_name = tag.get('property', '').lower()
        content = tag.get('content', '')
        
        if name == 'description':
            metadata['description'] = content
        elif name == 'keywords':
            metadata['keywords'] = content
        elif name == 'author':
            metadata['author'] = content
        elif property_name.startswith('og:'):
            metadata['open_graph'][property_name[3:]] = content
        elif name.startswith('twitter:'):
            metadata['twitter_cards'][name[8:]] = content
        elif name or property_name:
            metadata['meta_tags'][name or property_name] = content
    
    # Extract canonical URL
    canonical = soup.find('link', rel='canonical')
    if canonical:
        metadata['canonical_url'] = canonical.get('href')
    
    # Extract JSON-LD structured data
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            metadata['schema_org'].append(data)
        except:
            pass
    
    if include_technical:
        metadata['technical'] = {
            'total_links': len(soup.find_all('a')),
            'total_images': len(soup.find_all('img')),
            'total_scripts': len(soup.find_all('script')),
            'total_stylesheets': len(soup.find_all('link', rel='stylesheet')),
            'has_forms': len(soup.find_all('form')) > 0,
            'language': soup.get('lang') or soup.find('html', lang=True),
        }
    
    return metadata

async def main():
    """Main entry point"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced MCP Web Scraper")
    asyncio.run(main())
