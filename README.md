# 🛡️ Proxy Scraper & Validator

This Python script automatically downloads, cleans and validates proxy servers (HTTP, HTTPS, SOCKS4, SOCKS5) from public sources. It saves only **valid and working proxies** to separate files.

## 📦 Features

- 📥 Download proxies from popular GitHub sources
- 🧹 Remove duplicates
- ⚙️ Support types: `http`, `https`, `socks4`, `socks5`.
- ✅ Multithreaded check of working proxies
- 💾 Saving all and valid proxies to different files
- 🧠 Easy to use via CLI

---
run via: `python proxy_scraper.py <proxy_type>`.

---
## 🔧 Installation

1. Install Python (if not already installed)
2. Install the required libraries:

```bash
pip install requests 
