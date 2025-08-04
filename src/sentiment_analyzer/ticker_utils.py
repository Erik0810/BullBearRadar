import re
import yfinance as yf
from typing import List, Set
import logging

class TickerExtractor:
    """A class to extract and validate stock tickers from text."""
    
    def __init__(self):
        """Initialize the TickerExtractor with regex pattern for stock tickers."""
        # Pattern matches 1-5 uppercase letters, not surrounded by letters/numbers
        # Excludes common words that might look like tickers
        # Pattern matches 2-5 uppercase letters, not surrounded by letters/numbers
        # Single letter tickers are extremely rare and often false positives
        self.ticker_pattern = r'(?<![A-Za-z0-9])[A-Z]{2,5}(?![A-Za-z0-9])'
        
        # Common words and financial/technical terms that shouldn't be treated as tickers
        self.common_words = {
            # Common English words
            'I', 'A', 'THE', 'IN', 'ON', 'AT', 'TO', 'FOR', 'AND', 'OR',
            'BUT', 'SO', 'PM', 'AM', 'CEO', 'CFO', 'CTO', 'USA', 'UK','TEAM',
            'TALK', 'NEW','LOT','EDIT',
            # Financial/Market Terms
            'IPO', 'ETF', 'MACD', 'RSI', 'EPS', 'P2P', 'ROI', 'ROE', 'ROA',
            'EBIT', 'CAGR', 'WACC', 'GAAP', 'NYSE', 'DJIA', 'NASDAQ', 'DOW',
            'REIT', 'DRIP', 'FIFO', 'LIFO', 'FDIC', 'RICO', 'FANG', 'SPAC',
            # Technical Terms
            'API', 'AI', 'ML', 'CPU', 'GPU', 'RAM', 'SSD', 'HDD','PC','APP',
            'WWW',
            # Units and Others
            'USD', 'EUR', 'GBP', 'YTD', 'TTM', 'QOQ', 'YOY', 'FY',
            'Q1', 'Q2', 'Q3', 'Q4', 'FED', 'SEC', 'IMF', 'GDP'
        }
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def extract_potential_tickers(self, text: str) -> Set[str]:
        """
        Extract potential stock tickers from text using regex.
        
        Args:
            text (str): Text to extract tickers from
            
        Returns:
            Set[str]: Set of unique potential ticker symbols
        """
        try:
            # Find all matches of the ticker pattern
            matches = re.findall(self.ticker_pattern, text)
            # Filter out common words and create a set of unique tickers
            potential_tickers = {
                ticker for ticker in matches 
                if ticker not in self.common_words
            }
            return potential_tickers
        except Exception as e:
            self.logger.error(f"Error extracting tickers: {str(e)}")
            return set()

    def validate_ticker(self, ticker: str) -> bool:
        """
        Validate if a ticker exists on Yahoo Finance.
        
        Args:
            ticker (str): Ticker symbol to validate
            
        Returns:
            bool: True if ticker is valid, False otherwise
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Debug logging
            self.logger.debug(f"Validating ticker {ticker}")
            if not info:
                self.logger.debug(f"Ticker {ticker} has no info")
                return False
            
            # Check for specific fields that real stocks should have
            required_fields = ['symbol', 'regularMarketPrice', 'quoteType']
            has_required_fields = all(field in info for field in required_fields)
            
            if not has_required_fields:
                missing_fields = [f for f in required_fields if f not in info]
                self.logger.debug(f"Ticker {ticker} missing required fields: {missing_fields}")
                return False
            
            # Check if it's an equity/stock
            quote_type = info.get('quoteType', '')
            if quote_type != 'EQUITY':
                self.logger.debug(f"Ticker {ticker} is not an equity: {quote_type}")
                return False

            # Validate market price and symbol
            market_price = info.get('regularMarketPrice', 0)
            symbol_matches = info.get('symbol', '').upper() == ticker.upper()
            
            if not market_price or not symbol_matches:
                self.logger.debug(f"Ticker {ticker} failed price/symbol validation")
                return False
                
            return True
        except Exception as e:
            self.logger.error(f"Error validating ticker {ticker}: {str(e)}")
            return False

    def get_valid_tickers(self, text: str) -> List[str]:
        """
        Extract and validate stock tickers from text.
        
        Args:
            text (str): Text to extract tickers from
            
        Returns:
            List[str]: List of valid ticker symbols found in text
        """
        try:
            # Extract potential tickers
            potential_tickers = self.extract_potential_tickers(text)
            self.logger.debug(f"Potential tickers found: {potential_tickers}")
            
            # Validate each potential ticker
            valid_tickers = []
            for ticker in potential_tickers:
                if self.validate_ticker(ticker):
                    valid_tickers.append(ticker)
                    self.logger.debug(f"Validated ticker: {ticker}")
            
            self.logger.info(f"Found {len(valid_tickers)} valid tickers: {valid_tickers}")
            return valid_tickers
            
        except Exception as e:
            self.logger.error(f"Error in get_valid_tickers: {str(e)}")
            return []