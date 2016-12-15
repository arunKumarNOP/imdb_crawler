Overview
====
A Scrapy project coded in python to crawl Imdb website and construct the recommendation database which can be used for various purposes and analysis.
<br>
With this project you can get a basic ideas such as:

* Implementing a User-Agent switcher for scrapy crawler (using Middleware)
* Saving crawled data in a database, here SQLite is used (using Pipeline)
* Using different Item holder for different type of data
* Implementing Pause and Resume feature, by serialization and deserialization

Installation
====
You need scrapy and python 2.7 to run this project.

Install python for your platform and then install scrapy with:

<pre>sudo pip install scrapy</pre>

Usage
====
Navigate to top of the project directory and start the crawl with:

<pre>scrapy crawl imdb -s SAVE_FOLDER="crawled_data" -s FILE_NAME="sample_movie_ids"</pre>

SAVE_FOLDER is the folder name where to save the crawled information and <br> FILE_NAME is the file which contains the list of starting movie ids

A sample file named "sample_movie_ids" which contains movie ids.

A movie id is extracted from the imdb url.

Ex:

Imdb url: http://www.imdb.com/title/tt0120338
movie_id: tt0120338

