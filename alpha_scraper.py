import requests
import json
from config import get_config
from logger import log
from store import save
import time

name = "alpha_scraper"
config = get_config(name)

def scrape_historic_daily_time_series(symbol):
    log(name, f"Scrapping {symbol}")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={config['api_key']}&outputsize=full"
    response = requests.get(url)
    data = json.dumps(response.json()["Time Series (Daily)"])
    save(f"{symbol}_Daily.txt", data, 'w')
    log(name, f"{symbol} Dump file saved.")

def scrape_symbols():
    request_count = 0 # limit: 5 per minute
    for symbol in config["scrape_symbols"]:
        if(request_count >= 5):
            #Sleep for 1 minute before requesting again
            log(name, "60 second API Cooldown")
            time.sleep(60)
            request_count = 0
        scrape_historic_daily_time_series(symbol)
        request_count+= 1

scrape_symbols()
