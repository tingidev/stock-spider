## news_item/news_scraper/connect_mongo.py

import os
import configparser
from pymongo import MongoClient

class MongoDB:    
    """
    Connect to MongoDB. It opens connection and closes the connection when it is destroyed.
    """
    def __init__(self):
        self.config=configparser.ConfigParser()
        self.config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings.cfg'))
        #self.config.read_file(open('settings.cfg'))
        self.cnx = None

    def __enter__(self):
        print("enter")
        if self.cnx is not None:
            raise RunTimeError('Already connected')
        self.cnx = MongoClient(host=self.config.get('MONGODB','HOST'),
                    port=int(self.config.get('MONGODB','PORT')),
                    authSource=self.config.get('MONGODB','AUTHSOURCE'),
                    username=self.config.get('MONGODB','USERNAME'),
                    password=self.config.get('MONGODB','PASSWORD') )
        return self.cnx[self.config["MONGODB"]["DB"]]

    def __exit__(self, exe_ty, exc_val, tb):
    	self.cnx.close()
    	self.cnx = None