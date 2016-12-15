# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from imdb.items import ImdbItem, MovieItem

class ImdbSQLitePipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        filename = settings.get("FILE_NAME")
        save_folder = settings.get("SAVE_FOLDER")
        return cls(filename,save_folder)

    def __init__(self, filename, save_folder):
        file_path = './{0}/imdb_{1}.db'.format(save_folder,filename)
        self.conn = sqlite3.connect(file_path)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS imdb
            (movie_id VARCHAR(15) PRIMARY KEY, recommendations TEXT)''')

        self.cur.execute('CREATE TABLE IF NOT EXISTS movie_details(movie_id VARCHAR(15) PRIMARY KEY, movie_name TEXT NOT NULL)')

    def process_item(self, item, spider):
        if(isinstance(item,ImdbItem)):
            self.cur.execute("INSERT INTO imdb(movie_id, recommendations) VALUES (?, ?)",
                                    (item['movie_id'], item['recommen_id']))
            self.conn.commit()

        elif(isinstance(item,MovieItem)):
            try:
                self.cur.execute("INSERT INTO movie_details(movie_id, movie_name) VALUES (?, ?)", (item['movie_id'],item['movie_name']))
                self.conn.commit()
            except Exception, e:
                pass
        return item

    def handle_error(self, e):
        #log.err(e)
        pass

    def __del__(self):
        self.conn.close()