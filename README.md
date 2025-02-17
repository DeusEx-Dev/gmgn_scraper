# GMGN Token Scraper

A Python tool to fetch and standardize token data from GMGN.ai. Currently supports Solana tokens.

## Prerequisites

- Python 3.9+
- Git

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/gmgn-scraper.git
cd gmgn-scraper
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:

```bash
playwright install firefox
```

## Usage

Run the script and input a Solana token address when prompted:

```bash
python search_token_address.py
```

The script will:

Ask you to input a token address
Fetch the token data from GMGN.ai
Save the standardized data to token_data.json

**Example token data includes:**

- Token information (name, symbol, supply)
- Security analysis
- Dev analysis
- Rug check
- Holder statistics
- Social media links
- Wallet tags
