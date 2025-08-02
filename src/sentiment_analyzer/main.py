import os
from datetime import datetime
import logging
import pandas as pd
from dotenv import load_dotenv
from typing import List, Tuple, Callable, Optional
import csv

from .reddit_scraper import RedditScraper
from .ticker_utils import TickerExtractor
from .sentiment_analyzer import SentimentAnalyzer

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_or_create_sentiment_log() -> pd.DataFrame:
    """Load existing sentiment log or create a new one if it doesn't exist."""
    columns = ['Date', 'Top 3 Bullish', 'Top 3 Bearish']
    
    try:
        if os.path.exists('sentiment_log.csv'):
            return pd.read_csv('sentiment_log.csv')
        else:
            return pd.DataFrame(columns=columns)
    except Exception as e:
        logger.error(f"Error loading sentiment log: {str(e)}")
        return pd.DataFrame(columns=columns)

def format_ticker_list(tickers: List[str]) -> str:
    """Format list of tickers into comma-separated string."""
    return ', '.join(tickers) if tickers else ''

def save_results(bullish: List[str], bearish: List[str]):
    """Save results to sentiment_log.csv."""
    try:
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Format data
        new_row = {
            'Date': today,
            'Top 3 Bullish': format_ticker_list(bullish),
            'Top 3 Bearish': format_ticker_list(bearish)
        }
        
        # Load existing data
        df = load_or_create_sentiment_log()
        
        # Append new results
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Save to CSV
        df.to_csv('sentiment_log.csv', index=False)
        logger.info("Results saved successfully")
        
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")

def main(progress_callback: Optional[Callable[[str], None]] = None) -> Tuple[List[str], List[str]]:
    """Main function to orchestrate the Reddit sentiment analysis workflow."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize components
        reddit_scraper = RedditScraper(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        
        ticker_extractor = TickerExtractor()
        sentiment_analyzer = SentimentAnalyzer()
        
        # Update progress and fetch Reddit posts
        if progress_callback:
            progress_callback({"step": "fetching_posts", "message": "Fetching posts from r/stocks...", "progress": 5})
        logger.info("Fetching posts from r/stocks...")
        posts = reddit_scraper.get_top_daily_posts()
        
        if not posts:
            logger.error("No posts fetched from Reddit")
            return [], []
            
        total_posts = len(posts)
        if progress_callback:
            progress_callback({
                "step": "processing_posts",
                "message": "Found {} posts to analyze".format(total_posts),
                "progress": 10
            })
        
        # Process each post
        all_tickers = set()
        combined_text = ""
        
        for idx, post in enumerate(posts, 1):
            # Update progress for post processing
            if progress_callback:
                post_progress = 10 + (40 * (idx / total_posts))  # Progress from 10% to 50%
                progress_callback({
                    "step": "processing_posts",
                    "message": "Processing post {} of {}".format(idx, total_posts),
                    "progress": post_progress
                })
                
            # Combine title and body for analysis
            post_text = f"{post['title']} {post['body']}"
            combined_text += f" {post_text}"
            
            # Extract tickers from post
            tickers = ticker_extractor.get_valid_tickers(post_text)
            all_tickers.update(tickers)
        
        if not all_tickers:
            logger.error("No valid tickers found in posts")
            return [], []
        
        # Update progress and analyze sentiment
        if progress_callback:
            progress_callback({
                "step": "processing_tickers",
                "message": "Processing {} found tickers...".format(len(all_tickers)),
                "progress": 60
            })
        logger.info("Analyzing sentiment for {} tickers...".format(len(all_tickers)))
        ticker_sentiments = sentiment_analyzer.analyze_ticker_sentiment(
            combined_text, 
            list(all_tickers)
        )
        
        # Update progress for sentiment analysis
        if progress_callback:
            progress_callback({
                "step": "analyzing_sentiment",
                "message": "Analyzing sentiment...",
                "progress": 80
            })
            
        # Get top bullish and bearish tickers
        bullish, bearish = sentiment_analyzer.get_top_sentiments(ticker_sentiments)
        
        # Update progress and save results
        if progress_callback:
            progress_callback({
                "step": "saving_results",
                "message": "Saving results...",
                "progress": 95
            })
        logger.info("Saving results...")
        save_results(bullish, bearish)
        
        logger.info("Analysis completed successfully")
        logger.info(f"Top Bullish: {', '.join(bullish)}")
        logger.info(f"Top Bearish: {', '.join(bearish)}")
        
        return bullish, bearish
        
    except Exception as e:
        logger.error(f"Error in main workflow: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        bullish, bearish = main()
        print(f"\nTop Bullish: {', '.join(bullish)}")
        print(f"Top Bearish: {', '.join(bearish)}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)