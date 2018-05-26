# news_item/app.py

# Script to pull and email top daily stock listing scrape from MongoDB

from news_scraper import scrape_news

if __name__ == '__main__':
	scrape_news()