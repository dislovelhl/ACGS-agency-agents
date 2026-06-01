---
id: scrapling
name: Scrapling
description: Adaptive Python web scraping and crawling framework with resilient selectors, HTTP and browser fetchers, stealth sessions, proxy rotation, spider workflows, CLI extraction, and an MCP server for AI-assisted data extraction.
source_url: https://github.com/D4Vinci/Scrapling
install: pip install "scrapling[all]"
commands:
  - scrapling extract get 'https://example.com' content.md
  - scrapling extract get 'https://example.com' content.txt --css-selector '#products' --impersonate 'chrome'
  - scrapling shell
python_api:
  - from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
  - page = Fetcher.get("https://example.com/")
  - items = page.css(".product", adaptive=True)
capabilities:
  - web-scraping
  - web-crawling
  - adaptive-selectors
  - browser-automation
  - anti-bot-fetching
  - mcp-server
  - data-extraction
formats:
  - html
  - markdown
  - text
  - json
  - jsonl
keywords:
  - scrape
  - scraping
  - crawl
  - crawling
  - website
  - web
  - dynamic
  - browser
  - stealth
  - selectors
  - css
  - xpath
  - adaptive
  - products
  - extraction
  - mcp
  - proxy
  - robots
security_notes:
  - Use only for lawful scraping, public-data collection, owned sites, or targets where you have permission.
  - Respect robots.txt, site terms, privacy law, rate limits, and data minimization requirements.
  - Treat URLs, selectors, proxy settings, and extracted content as untrusted input.
  - Do not use stealth or anti-bot features to evade access controls, authentication, paywalls, or explicit denial of permission.
  - Browser and fetcher modes perform network I/O and may execute remote page code; run in constrained environments for untrusted sites.
use_when:
  - An agent needs to extract structured content from websites, including dynamic pages.
  - An agent needs resilient CSS/XPath selectors that survive layout changes.
  - An agent needs crawling, pause/resume, proxy rotation, or an MCP-assisted scraping workflow.
avoid_when:
  - The target forbids scraping or the agent lacks authorization.
  - The task only needs local file parsing, document conversion, or simple repo search.
  - Network execution cannot be sandboxed for untrusted pages.
---

# Scrapling

Use Scrapling when an agent needs adaptive web scraping, crawling, dynamic browser fetching, or an AI/MCP-oriented data extraction workflow.
