import os
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

class MarketDataService:
    def __init__(self):
        self.alpha_vantage_key = os.environ.get('ALPHA_VANTAGE_API_KEY') or os.environ.get('ALPHA_VANTAGE_KEY')
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        try:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.alpha_vantage_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                return {
                    "symbol": symbol,
                    "price": float(quote.get("05. price", 0)),
                    "change_percent": float(quote.get("10. change percent", "0%").replace("%", "")),
                    "volume": float(quote.get("06. volume", 0))
                }
            return {"symbol": symbol, "price": 0, "change_percent": 0}
        except Exception as e:
            print(f"Error fetching stock quote: {e}")
            return {"symbol": symbol, "price": 0, "change_percent": 0}
    
    def get_market_overview(self) -> List[Dict[str, Any]]:
        # Get quotes for major indices and popular stocks
        symbols = ["SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
        overview = []
        
        for symbol in symbols:
            quote = self.get_stock_quote(symbol)
            if quote["price"] > 0:
                overview.append(quote)
        
        return overview
    
    def get_crypto_prices(self) -> List[Dict[str, Any]]:
        # Mock crypto data since CoinGecko requires premium for some features
        return [
            {"symbol": "BTC", "name": "Bitcoin", "price": 45000, "change_percent": 2.5},
            {"symbol": "ETH", "name": "Ethereum", "price": 2800, "change_percent": 3.2},
            {"symbol": "BNB", "name": "Binance Coin", "price": 350, "change_percent": -1.2},
        ]
    
    def get_forex_rate(self, from_currency: str, to_currency: str) -> Dict[str, Any]:
        try:
            params = {
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": from_currency,
                "to_currency": to_currency,
                "apikey": self.alpha_vantage_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if "Realtime Currency Exchange Rate" in data:
                rate_data = data["Realtime Currency Exchange Rate"]
                return {
                    "from": from_currency,
                    "to": to_currency,
                    "rate": float(rate_data.get("5. Exchange Rate", 0)),
                    "timestamp": rate_data.get("6. Last Refreshed", "")
                }
            return {"from": from_currency, "to": to_currency, "rate": 0}
        except Exception as e:
            print(f"Error fetching forex rate: {e}")
            return {"from": from_currency, "to": to_currency, "rate": 0}
