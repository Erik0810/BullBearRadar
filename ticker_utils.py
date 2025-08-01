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
        self.ticker_pattern = r'(?<![A-Za-z0-9])[A-Z]{1,5}(?![A-Za-z0-9])'
        self.common_words = {
            'I', 'A', 'THE', 'IN', 'ON', 'AT', 'TO', 'FOR', 'AND', 'OR',
            'BUT', 'SO', 'PM', 'AM', 'CEO', 'CFO', 'CTO', 'USA', 'UK'
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
            # Try to get info - returns empty dict if ticker doesn't exist
            info = stock.info
            return bool(info)
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
            
            # Validate each potential ticker
            valid_tickers = [
                ticker for ticker in potential_tickers
                if self.validate_ticker(ticker)
            ]
            
            self.logger.info(f"Found {len(valid_tickers)} valid tickers")
            return valid_tickers
            
        except Exception as e:
            self.logger.error(f"Error in get_valid_tickers: {str(e)}")
            return []