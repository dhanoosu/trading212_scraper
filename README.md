# trading212_scraper
Python based web scraping using selenium for extracting current portfolio holdings.

- Currently only support Edge driver
- Supports Python2.7 / Python3.1+

Trading212 is a great online broker for trading CFDs and stock investments. Although it has a built-in portfolio tracking of holdings, it is not very versatile. This script will help extract current holdings of `free_fund`, `account_value`, `market_value`, `buy_price`, `sell_price`, `ticker name` etc. - you can then export this to something like Google Sheets and make your custom Portfolio tracking.

## Installation and Pre-requisites

Clone this tool by:

    git clone https://github.com/dhanoosu/trading212_scraper.git

The followings are needed to be installed
```
$> pip install selenium
$> pip install msedge-selenium-tools
```

## Trading212 Setup

Make sure the following show tabs setting are checked, and that 2 Factor-Authenication is disabled.

<img src="img/show_tabs_settings.jpg" width="220">

## Usage

```python
from src.trading212_scraper import Scrape
```

Initialise a new class object, parsing in your username and password.
`headless=True` allows the active window to be run in background.

```python
trading212 = Scrape(
  username = <YOUR_USERNAME>,
  password = <YOUR_PASSWORD>,
  headless = <True/False>
)

try:
    trading212.setup()

    trading212.scrape(account=<"ISA"/"INVESTING">)

    account_summary = trading212.get_account_summary()
    stocks = trading212.get_stocks()
    
finally:

    #Gracefully exit the driver
    trading212.close_driver()

```

## Known Issues
- Once in a while, you might experience a `StaleElementException` - simply restart the script

## Support [![Buy me a coffee](https://img.shields.io/badge/-buy%20me%20a%20coffee-lightgrey?style=flat&logo=buy-me-a-coffee&color=FF813F&logoColor=white "Buy me a coffee")](https://www.buymeacoffee.com/dhanoosu)
If you like this tool, consider [buying me a coffee](https://www.buymeacoffee.com/dhanoosu) to support the development of this.
