import nltk
from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Tuple
import logging
from statistics import mean

class SentimentAnalyzer:
    """A class to analyze sentiment of text containing stock tickers."""
    
    def __init__(self):
        """Initialize the SentimentAnalyzer with VADER sentiment analyzer."""
        self.vader = SentimentIntensityAnalyzer()
        self.tokenizer = sent_tokenize
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_text_sentiment(self, text: str) -> float:
        """
        Get the compound sentiment score for a piece of text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            float: Compound sentiment score (-1 to 1)
        """
        try:
            scores = self.vader.polarity_scores(text)
            return scores['compound']
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return 0.0

    def get_sentences_with_ticker(self, text: str, ticker: str) -> List[str]:
        """
        Extract sentences that contain a specific ticker symbol.
        
        Args:
            text (str): Full text to process
            ticker (str): Ticker symbol to look for
            
        Returns:
            List[str]: List of sentences containing the ticker
        """
        try:
            # Split text into sentences
            sentences = self.tokenizer(text)
            
            # Return sentences containing the ticker
            return [
                sentence for sentence in sentences
                if ticker in sentence
            ]
        except Exception as e:
            self.logger.error(f"Error extracting sentences: {str(e)}")
            return []

    def analyze_ticker_sentiment(self, text: str, tickers: List[str]) -> Dict[str, float]:
        """
        Analyze sentiment for each ticker in the text.
        
        Args:
            text (str): Text to analyze
            tickers (List[str]): List of ticker symbols to analyze
            
        Returns:
            Dict[str, float]: Dictionary mapping tickers to their sentiment scores
        """
        try:
            ticker_sentiments: Dict[str, List[float]] = {ticker: [] for ticker in tickers}
            
            # Process each ticker
            for ticker in tickers:
                # Get sentences containing the ticker
                relevant_sentences = self.get_sentences_with_ticker(text, ticker)
                
                # Analyze sentiment for each relevant sentence
                for sentence in relevant_sentences:
                    sentiment = self.get_text_sentiment(sentence)
                    ticker_sentiments[ticker].append(sentiment)
            
            # Calculate average sentiment for each ticker
            return {
                ticker: mean(scores) if scores else 0.0
                for ticker, scores in ticker_sentiments.items()
            }
            
        except Exception as e:
            self.logger.error(f"Error in ticker sentiment analysis: {str(e)}")
            return {ticker: 0.0 for ticker in tickers}

    def get_top_sentiments(self, 
                          ticker_sentiments: Dict[str, float], 
                          top_n: int = 3) -> Tuple[List[str], List[str]]:
        """
        Get top bullish and bearish tickers based on sentiment scores.
        
        Args:
            ticker_sentiments (Dict[str, float]): Dictionary of ticker sentiments
            top_n (int): Number of top tickers to return (default: 3)
            
        Returns:
            Tuple[List[str], List[str]]: Lists of top bullish and bearish tickers
        """
        try:
            # Sort tickers by sentiment score
            sorted_tickers = sorted(
                ticker_sentiments.items(), 
                key=lambda x: x[1],
                reverse=True
            )
            
            # Split into bullish and bearish
            bullish = [ticker for ticker, _ in sorted_tickers[:top_n]]
            bearish = [ticker for ticker, _ in sorted_tickers[-top_n:]]
            bearish.reverse()  # Most bearish first
            
            return bullish, bearish
            
        except Exception as e:
            self.logger.error(f"Error getting top sentiments: {str(e)}")
            return [], []