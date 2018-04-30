# Script to pull and email top daily stock listing scrape from MongoDB

from daily_listing_emailer import email_last_scraped_listing

if __name__ == '__main__':
	email_last_scraped_listing()