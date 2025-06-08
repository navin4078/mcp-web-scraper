#!/bin/bash
# setup.sh - Simple installation script for MCP Web Scraper

echo "🚀 Setting up MCP Web Scraper..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Create virtual environment
echo "🔦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Get the absolute path to the MCP script
SCRIPT_PATH="$(pwd)/app_mcp.py"
PYTHON_PATH="$(pwd)/venv/bin/python"

echo "
✅ Setup completed successfully!

🔧 Claude Desktop Configuration:

1. Open your Claude Desktop config file:
   - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
   - Windows: %APPDATA%\\Claude\\claude_desktop_config.json
   - Linux: ~/.config/Claude/claude_desktop_config.json

2. Add this simple configuration:

{
  \"mcpServers\": {
    \"web-scraper\": {
      \"command\": \"$PYTHON_PATH\",
      \"args\": [\"$SCRIPT_PATH\"]
    }
  }
}

3. Restart Claude Desktop completely

4. Look for the hammer icon (🔨) in Claude Desktop

💯 That's it! No web server, no mcp-proxy, no extra complexity!

💡 The MCP server will start automatically when Claude Desktop needs it.

📝 Available tools:
   - scrape_website: Extract text, links, images, or tables
   - extract_headlines: Get all headlines from a page  
   - extract_metadata: Get page metadata and Open Graph tags
   - get_page_info: Get basic page statistics

🕷️ Ready to start web scraping with Claude!
"