# news_item/news_scraper/__init__.py

# import os
# import time
import newspaper

from newspaper import news_pool
from .connect_mongo import MongoDB
from datetime import datetime as dt
#from mongoengine import connect

def scrape_news():

    #t = time.time()

    ## connect
    client = MongoDB()

    with client as db:

        # #connect (not necessary)
        # connect(db)

        ## multi-threading
        eu_paper = newspaper.build('https://theguardian.com', memoize_articles=False, fetch_images=False)
        us_paper = newspaper.build('https://www.cbsnews.com/', memoize_articles=False, fetch_images=False)
        hk_paper = newspaper.build('http://scmp.com', memoize_articles=False, fetch_images=False)
        jp_paper = newspaper.build('https://www.japantimes.co.jp/', memoize_articles=False, fetch_images=False)

        papers = [eu_paper, us_paper, hk_paper, jp_paper]
        news_pool.set(papers, threads_per_source=2) # (4*2) = 8 threads total
        news_pool.join()

        print("Size of EU paper: " + str(eu_paper.size()))
        print("Size of US paper: " + str(us_paper.size()))
        print("Size of HK paper: " + str(hk_paper.size()))
        print("Size of JP paper: " + str(jp_paper.size()))

        for paper in papers:
            for article in paper.articles:
                try:
                    article.parse()
                    print(len(article.text))
                    if len(article.text) > 100:
                        article.nlp()
                        item = {
                            'url': article.url,
                            'brand': paper.brand,
                            'title': article.title,
                            'text': article.text,
                            'keywords': article.keywords,
                            'summary': article.summary,
                            'date': dt.today(),
                            'date_str': dt.today().strftime('%Y-%m-%d')
                        }
                        db.news_items.insert_one(item)
                except Exception as e:
                    #In case it fails, skip article
                    print(e)
                    print("continuing...")
                    continue
# print('Finished!')
# elapsed = time.time() - t
# print(str(elapsed))
