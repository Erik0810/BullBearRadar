# Stock Sentiment Analyzer

A Python application that analyzes stock sentiment from Reddit's r/stocks subreddit by scraping daily top posts, extracting stock tickers, and performing sentiment analysis to identify the most bullish and bearish mentioned stocks.

## Features

- Scrapes top daily posts from r/stocks subreddit
- Extracts and validates stock tickers using Yahoo Finance
- Performs sentiment analysis using VADER
- Tracks top bullish and bearish stocks in a CSV log
- Filters out common English words that might look like tickers

## Prerequisites

- Python 3.6+
- Reddit API credentials (Client ID, Client Secret, and User Agent)

## Installation

1. Clone the repository
2. Install required packages:
```bash
pip install -r requirements.txt
```
3. Copy `.env.template` to `.env` and fill in your Reddit API credentials:
```bash
cp .env.template .env
```

## Configuration

Update the `.env` file with your Reddit API credentials:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

## Usage

Run the main script to analyze current stock sentiment:
```bash
python main.py
```

The script will:
1. Fetch top daily posts from r/stocks
2. Extract valid stock tickers
3. Analyze sentiment for each ticker
4. Save results to `sentiment_log.csv`

## Output

Results are saved to `sentiment_log.csv` with the following columns:
- Date: Analysis date
- Top 3 Bullish: Most positively mentioned tickers
- Top 3 Bearish: Most negatively mentioned tickers

## Dependencies

- praw: Reddit API wrapper
- yfinance: Yahoo Finance API
- vaderSentiment: Sentiment analysis
- pandas: Data manipulation
- nltk: Natural language processing
- python-dotenv: Environment variable management

## License

This project is open source and available under the MIT License.