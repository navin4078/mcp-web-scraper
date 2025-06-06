# MCP Web Scraper - Direct STDIO Implementation
# A simple and efficient web scraping MCP server using direct STDIO protocol

import asyncio
import logging
from typing import Dict, List, Any, Optional
import requests
from bs4 import BeautifulSoup
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
server = Server("web-scraper")

# Headers to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def fetch_and_parse(url: str) -> BeautifulSoup:
    """Fetch webpage and return BeautifulSoup object"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'lxml')
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch URL: {str(e)}")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="scrape_website",
            description="Scrape a website and extract data (text, links, images, or tables)",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to scrape"
                    },
                    "extract_type": {
                        "type": "string", 
                        "enum": ["text", "links", "images", "table"],
                        "description": "Type of data to extract",
                        "default": "text"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector to target specific elements (optional)"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="extract_headlines",
            description="Extract headlines (h1, h2, h3) from a webpage",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to extract headlines from"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="extract_metadata",
            description="Extract metadata from a webpage (title, description, keywords, Open Graph tags)",
            inputSchema={
                "type": "object", 
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to extract metadata from"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="get_page_info",
            description="Get basic information about a webpage (title, element counts, structure)",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string", 
                        "description": "The URL to analyze"
                    }
                },
                "required": ["url"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    
    if name == "scrape_website":
        return await scrape_website_tool(arguments)
    elif name == "extract_headlines":
        return await extract_headlines_tool(arguments)
    elif name == "extract_metadata":
        return await extract_metadata_tool(arguments)
    elif name == "get_page_info":
        return await get_page_info_tool(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def scrape_website_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Scrape website and extract data"""
    try:
        url = args["url"]
        extract_type = args.get("extract_type", "text")
        selector = args.get("selector")
        max_results = args.get("max_results", 10)
        
        soup = fetch_and_parse(url)
        title = soup.title.string if soup.title else "No title"
        
        data = []
        
        if extract_type == "text":
            elements = soup.select(selector) if selector else soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for elem in elements[:max_results]:
                text = elem.get_text(strip=True)
                if text:
                    data.append({
                        'text': text,
                        'tag': elem.name,
                        'class': elem.get('class', [])
                    })
        
        elif extract_type == "links":
            elements = soup.select(selector) if selector else soup.find_all('a', href=True)
            for elem in elements[:max_results]:
                data.append({
                    'text': elem.get_text(strip=True),
                    'href': elem.get('href'),
                    'title': elem.get('title', '')
                })
        
        elif extract_type == "images":
            elements = soup.select(selector) if selector else soup.find_all('img', src=True)
            for elem in elements[:max_results]:
                data.append({
                    'src': elem.get('src'),
                    'alt': elem.get('alt', ''),
                    'title': elem.get('title', '')
                })
        
        elif extract_type == "table":
            tables = soup.select(selector) if selector else soup.find_all('table')
            for table in tables[:max_results]:
                rows = table.find_all('tr')
                table_data = []
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    if row_data:
                        table_data.append(' | '.join(row_data))
                if table_data:
                    data.append({
                        'table_data': '\n'.join(table_data),
                        'rows': len(table_data)
                    })
        
        result = {
            'url': url,
            'title': title,
            'extract_type': extract_type,
            'count': len(data),
            'data': data
        }
        
        return [TextContent(type="text", text=f"Successfully scraped {url}\n\n" + str(result))]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error scraping website: {str(e)}")]

async def extract_headlines_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Extract headlines from webpage"""
    try:
        url = args["url"]
        soup = fetch_and_parse(url)
        title = soup.title.string if soup.title else "No title"
        
        headlines = soup.find_all(['h1', 'h2', 'h3'])
        data = []
        
        for headline in headlines:
            text = headline.get_text(strip=True)
            if text:
                data.append({
                    'text': text,
                    'tag': headline.name,
                    'class': headline.get('class', []),
                    'id': headline.get('id', '')
                })
        
        result = {
            'url': url,
            'title': title,
            'headlines_count': len(data),
            'headlines': data
        }
        
        return [TextContent(type="text", text=f"Headlines from {url}\n\n" + str(result))]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error extracting headlines: {str(e)}")]

async def extract_metadata_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Extract metadata from webpage"""
    try:
        url = args["url"]
        soup = fetch_and_parse(url)
        
        metadata = {
            'url': url,
            'title': soup.title.string if soup.title else None,
            'description': None,
            'keywords': None,
            'author': None,
            'og_title': None,
            'og_description': None,
            'og_image': None,
            'twitter_title': None,
            'twitter_description': None,
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
            elif property_name == 'og:title':
                metadata['og_title'] = content
            elif property_name == 'og:description':
                metadata['og_description'] = content
            elif property_name == 'og:image':
                metadata['og_image'] = content
            elif name == 'twitter:title':
                metadata['twitter_title'] = content
            elif name == 'twitter:description':
                metadata['twitter_description'] = content
        
        return [TextContent(type="text", text=f"Metadata from {url}\n\n" + str(metadata))]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error extracting metadata: {str(e)}")]

async def get_page_info_tool(args: Dict[str, Any]) -> List[TextContent]:
    """Get basic page information"""
    try:
        url = args["url"]
        soup = fetch_and_parse(url)
        
        # Extract basic info
        title = soup.title.string if soup.title else None
        meta_description = None
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            meta_description = meta_desc.get('content')
        
        # Count elements
        info = {
            'url': url,
            'title': title,
            'description': meta_description,
            'stats': {
                'paragraphs': len(soup.find_all('p')),
                'headings': len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])),
                'links': len(soup.find_all('a', href=True)),
                'images': len(soup.find_all('img')),
                'tables': len(soup.find_all('table')),
                'forms': len(soup.find_all('form'))
            }
        }
        
        return [TextContent(type="text", text=f"Page information for {url}\n\n" + str(info))]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error getting page info: {str(e)}")]

async def main():
    """Main entry point"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    logger.info("🕷️ Starting MCP Web Scraper (STDIO)")
    asyncio.run(main())