# MCP Web Scraper

A lightweight and efficient web scraping MCP server using direct STDIO protocol


## 🚀 Quick Start

### Option 1: Automated Setup

```bash
# Clone and setup
git clone https://github.com/navin4078/mcp-web-scraper
cd mcp-web-scraper
chmod +x setup.sh && ./setup.sh
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install minimal dependencies
pip install -r requirements.txt
```

## ⚙️ Claude Desktop Configuration

### Step 1: Find Your Paths

```bash
# Get absolute paths (run this in your project directory)
echo "Python path: $(pwd)/venv/bin/python"
echo "Script path: $(pwd)/app_mcp.py"
```

### Step 2: Configure Claude Desktop

Open your Claude Desktop config file:

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Step 3: Add Configuration

Add this to your config file:

```json
{
  "mcpServers": {
    "web-scraper": {
      "command": "/full/path/to/your/venv/bin/python",
      "args": ["/full/path/to/your/app_mcp.py"]
    }
  }
}
```

**Example:**
```json
{
  "mcpServers": {
    "web-scraper": {
      "command": "/Users/username/Desktop/scrapper/venv/bin/python",
      "args": ["/Users/username/Desktop/scrapper/app_mcp.py"]
    }
  }
}
```

### Step 4: Restart Claude Desktop

1. Completely close Claude Desktop (Cmd+Q on Mac)
2. Restart the application
3. Look for the hammer icon (🔨)
4. You should see "web-scraper" in your MCP servers

## 🛠 Available Tools

### **scrape_website**
Extract data from websites with flexible options:
- **extract_type**: `text`, `links`, `images`, `table`
- **selector**: CSS selector for targeting specific elements
- **max_results**: Limit number of results (1-50)

### **extract_headlines**
Get all headlines (h1, h2, h3) from a webpage with hierarchy and attributes.

### **extract_metadata**
Extract comprehensive metadata:
- Basic: title, description, keywords, author
- Open Graph: og:title, og:description, og:image
- Twitter Cards: twitter:title, twitter:description

### **get_page_info**
Get page structure overview:
- Element counts (paragraphs, headings, links, images, tables)
- Basic metadata
- Page statistics

## 💡 Usage Examples

### Basic Scraping
```
Scrape the text content from https://example.com

Extract all links from https://news.ycombinator.com

Get headlines from https://www.bbc.com/news
```

### Advanced Examples
```
Extract all images from https://example.com with their alt text

Scrape text from https://example.com using the CSS selector ".article-content p"

Get metadata and Open Graph tags from https://github.com

What's the page structure of https://stackoverflow.com?
```

### Specific Selectors
```
Extract text from https://news.ycombinator.com using selector ".titleline a"

Get all table data from https://example.com/data-page

Scrape only paragraph text from articles using selector "article p"
```

## 📁 Project Structure

```
scrapper/
├── app_mcp.py             # Main MCP server (STDIO)
├── requirements.txt       # Minimal dependencies
├── setup.sh              # Simple setup script
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Features

### Web Scraping Capabilities
- ✅ Text extraction with CSS selectors
- ✅ Link extraction with full attributes
- ✅ Image extraction with metadata
- ✅ Table data extraction and formatting
- ✅ Comprehensive metadata extraction
- ✅ Headline extraction with hierarchy
- ✅ Custom CSS selector support
- ✅ Configurable result limits
- ✅ Error handling and validation

### MCP Integration
- ✅ Direct STDIO protocol (no HTTP needed)
- ✅ Native Claude Desktop integration
- ✅ Automatic server lifecycle management
- ✅ Schema validation and documentation
- ✅ Comprehensive error handling
- ✅ Minimal dependencies

## 🛡 Security & Best Practices

1. **Respect robots.txt**: Always check robots.txt before scraping
2. **Rate limiting**: Built-in 10-second request timeout
3. **User-Agent**: Uses modern browser headers
4. **Input validation**: URL and parameter validation
5. **Error handling**: Graceful error handling and reporting
6. **Resource limits**: Configurable result limits prevent overload

## 🐛 Troubleshooting

### MCP Server Not Appearing

**Check your paths:**
```bash
# Verify files exist
ls -la /path/to/your/venv/bin/python
ls -la /path/to/your/app_mcp.py

# Test the script manually
/path/to/your/venv/bin/python /path/to/your/app_mcp.py
```

**Validate JSON configuration:**
- Use a JSON validator to check syntax
- Ensure no trailing commas
- Use absolute paths (not relative)

### Permission Issues

```bash
# Make script executable
chmod +x app_mcp.py

# Check virtual environment
source venv/bin/activate
python --version
```

### Import Errors

```bash
# Reinstall dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Testing the MCP Server

You can test if the server works by running it manually:
```bash
source venv/bin/activate
python app_mcp.py
```

The server should start and wait for STDIO input from Claude Desktop.

## 📚 Dependencies

- **requests**: HTTP library for web requests
- **beautifulsoup4**: HTML/XML parsing
- **lxml**: Fast XML and HTML processor  
- **mcp**: Model Context Protocol library



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test thoroughly with Claude Desktop
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Claude Desktop](https://claude.ai/download)

---

**Simple, efficient web scraping for Claude Desktop! 🕷️✨**
