import yfinance as yf
from typing import Dict, Any
import logging

class StockData:
    """Class to fetch and manage stock financial data using Yahoo Finance."""
    
    def __init__(self):
        """Initialize StockData with logger setup."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def get_stock_history(self, ticker: str) -> Dict[str, Any]:
        """
        Get historical data and key statistics for a stock.
        
        Args:
            ticker (str): The stock ticker symbol
            
        Returns:
            Dict containing:
            - name: Company name
            - price: Current price
            - market_cap: Market capitalization
            - pe_ratio: Price to Earnings ratio
            - history: DataFrame with historical price data
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            history = stock.history(period="1y")  # Get 1 year of data
            
            return {
                "name": info.get("longName", ticker),
                "price": info.get("regularMarketPrice", 0),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("forwardPE", 0),
                "history": history
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {ticker}: {str(e)}")
            return None