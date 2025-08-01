import praw
from datetime import datetime, timedelta
from typing import List, Dict

class RedditScraper:
    """A class to handle scraping Reddit posts from r/stocks."""
    
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """
        Initialize the RedditScraper with Reddit API credentials.
        
        Args:
            client_id (str): Reddit API client ID
            client_secret (str): Reddit API client secret
            user_agent (str): Unique user agent string for the bot
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.subreddit = self.reddit.subreddit('stocks')

    def get_top_daily_posts(self, limit: int = 50) -> List[Dict]:
        """
        Fetch top daily posts from r/stocks.
        
        Args:
            limit (int): Number of posts to fetch (default: 50)
            
        Returns:
            List[Dict]: List of dictionaries containing post data
                Each dict contains:
                - title: Post title
                - body: Post body text
                - score: Post score (upvotes - downvotes)
                - created_utc: Post creation timestamp
        """
        posts = []
        try:
            # Get top posts from the last 24 hours
            for submission in self.subreddit.top('day', limit=limit):
                post_data = {
                    'title': submission.title,
                    'body': submission.selftext,
                    'score': submission.score,
                    'created_utc': datetime.fromtimestamp(submission.created_utc)
                }
                posts.append(post_data)
                
        except Exception as e:
            print(f"Error fetching posts: {str(e)}")
            return []
            
        return posts

    def __str__(self) -> str:
        """Return string representation of the scraper."""
        return f"RedditScraper(subreddit=r/stocks)"