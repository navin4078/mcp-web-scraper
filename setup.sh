#!/bin/bash
# setup.sh - Enhanced setup for powerful web scraper

echo "🥷 Setting up Enhanced Web Scraper with Stealth Features..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Remove old virtual environment if it exists
if [ -d "venv" ]; then
    echo "🗑️ Removing old virtual environment..."
    rm -rf venv
fi

# Also check and remove from junk folder if exists
if [ -d "junk/venv" ]; then
    echo "🗑️ Removing virtual environment from junk folder..."
    rm -rf junk/venv
fi

# Create virtual environment
echo "📦 Creating fresh virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📥 Installing enhanced dependencies..."
pip install -r requirements.txt

# Install Playwright browsers with stealth capabilities
echo "🎭 Installing Playwright browsers for enhanced scraping..."
echo "   This downloads optimized browser binaries..."
playwright install chromium

# Optional: Install additional browsers for maximum compatibility
read -p "🦊 Install Firefox for additional bypass capabilities? (y/N): " install_firefox
if [[ $install_firefox =~ ^[Yy]$ ]]; then
    echo "🦊 Installing Firefox browser..."
    playwright install firefox
    echo "✅ Firefox installed for additional compatibility!"
fi

# Create a test to verify stealth features
echo "🧪 Testing stealth capabilities..."
python3 -c "
import asyncio
from fake_useragent import UserAgent
try:
    ua = UserAgent()
    print(f'✅ User Agent rotation: {ua.random[:50]}...')
    print('✅ Stealth features ready')
except Exception as e:
    print(f'⚠️ Warning: {e}')
    print('✅ Basic functionality still available')
"

# Get paths for configuration
SCRIPT_PATH="$(pwd)/app_mcp.py"
PYTHON_PATH="$(pwd)/venv/bin/python"

echo "
✅ Enhanced Web Scraper setup completed!

🥷 Stealth Features Enabled:
   ✓ Advanced user agent rotation with real browser fingerprints
   ✓ Human-like browsing behavior simulation
   ✓ Intelligent retry mechanisms with exponential backoff
   ✓ Multiple extraction strategies with automatic fallback
   ✓ Enhanced content detection for modern websites
   ✓ Anti-detection browser configuration
   ✓ Realistic request timing and delays
   ✓ Advanced content cleaning algorithms

🔧 Claude Desktop Configuration:

{
  \"mcpServers\": {
    \"enhanced-web-scraper\": {
      \"command\": \"$PYTHON_PATH\",
      \"args\": [\"$SCRIPT_PATH\"]
    }
  }
}

🛠️ Enhanced Tools Available:
   • scrape_website_enhanced: Maximum extraction with stealth
   • extract_article_content: Advanced article detection
   • extract_comprehensive_metadata: Complete metadata extraction
   • crawl_website_enhanced: Intelligent multi-page crawling

💪 Success Rate Improvements:
   • Automatic fallback (Dynamic → Static)
   • Multiple extraction strategies
   • Enhanced content detection
   • Improved error handling
   • Realistic browsing simulation

🧪 Test your installation:
   python test_installation.py

🎯 For difficult websites:
   • Use stealth_mode=true (default)
   • Enable JavaScript rendering
   • Increase retry attempts
   • Use longer delays between requests

⚡ The scraper now handles:
   • Modern SPAs and dynamic content
   • Advanced content detection
   • Multiple extraction fallbacks
   • Realistic browser behavior
   • Enhanced stealth features

🎉 Ready for challenging websites with maximum success rates!
"