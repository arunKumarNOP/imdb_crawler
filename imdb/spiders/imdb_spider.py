import scrapy
import os
from imdb.items import ImdbItem, MovieItem
from json import JSONEncoder,JSONDecoder

class ImdbSpider(scrapy.Spider):
    name = "imdb"
    folder_name = ''
    allowed_domains = ["www.imdb.com"]
    start_movie_id =[]
    start_urls = []

    base_url = "http://www.imdb.com/title/"
    crawled_set = set()
    to_crawl_set = set()

    json_encoder = JSONEncoder()
    json_decoder = JSONDecoder()

    fCrawled = ''
    fToCrawl =''

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        filename = settings.get("FILE_NAME")
        save_folder = settings.get("SAVE_FOLDER")
        return cls(filename,save_folder)


    def __init__(self,filename,save_folder):
        if not os.path.isdir(save_folder):
            os.mkdir(save_folder)
        if not os.path.isdir(os.path.join(save_folder , filename)):
                os.mkdir(os.path.join(save_folder , filename))

        self.folder_name = os.path.join(save_folder , filename)

        self.fCrawled = os.path.join(save_folder , 'crawled')
        self.fToCrawl = os.path.join(save_folder , 'to_crawl')

        self.restore_state(filename)

    def restore_state(self,filename):
        start_url_stored = set()
        crawled_stored = set()

        with open(filename) as f:
            start_url_stored = set(f.read().split(','))

        if os.path.isfile(self.fCrawled):
            with open(self.fCrawled) as f:
                crawled_stored = set(self.json_decoder.decode(f.read()))

        if os.path.isfile(self.fToCrawl):
            with open(self.fToCrawl) as f:
                self.to_crawl_set = set(self.json_decoder.decode(f.read()))

        self.crawled_set = crawled_stored

        # Remove already crawled movies from to_crawl_set
        self.to_crawl_set = self.to_crawl_set - crawled_stored

        # Constuct the list of movie_ids to start the crawl
        self.start_movie_id = start_url_stored.union(self.to_crawl_set) - crawled_stored


    def save_state(self):
        with open(self.fCrawled,'w') as f:
            f.write(self.json_encoder.encode(list(self.crawled_set)))

        with open(self.fToCrawl,'w') as f:
            f.write(self.json_encoder.encode(list(self.to_crawl_set)))


    def start_requests(self):
        for movie_id in self.start_movie_id:
            url = self.base_url + movie_id +'/'
            yield scrapy.Request(url,self.parse_movie)

    def parse_movie(self, response):
        movie_id = response.url.split("/")[-2]

        # Dont process the webpage if its already crawled
        if( movie_id in self.crawled_set ):
            return

        filename = os.path.join(self.folder_name, movie_id + ".html")

        if not os.path.isfile(filename):
            with open(filename,"wb") as f:
            	# Save the webpage
                f.write(response.body)

        movie_name = response.xpath("//h1[@class=''][@itemprop='name']/text()").extract_first().strip()
        recommendation_container = response.xpath("//div[@class='rec_slide']")
        recommendations_list = recommendation_container.xpath(".//a")

        self.crawled_set.add(movie_id)
        self.to_crawl_set.discard(movie_id)
        links_list =[]
        recommen_ids = []

        movieItem = MovieItem()
        movieItem['movie_id'] = movie_id
        movieItem['movie_name'] = movie_name
        yield movieItem

        for recommendation in recommendations_list:
            rec_movie_name = recommendation.xpath("./img/@title").extract_first()
            rec_movie_id = recommendation.xpath("./@href").extract_first().split('/')[2]
            if(rec_movie_name == '' or rec_movie_name == None):
                rec_movie_name = recommendation.xpath("./img/@alt").extract_first().strip()

            if( rec_movie_id not in self.crawled_set and rec_movie_id not in self.to_crawl_set ):
                self.to_crawl_set.add(rec_movie_id)
                next_url = self.base_url + rec_movie_id + "/"
                # Start a new request for the new encountered movie
                yield scrapy.Request(next_url, self.parse_movie)

            recommen_ids.append(rec_movie_id)

            # save the movie_id , movie_name pair in a global database
            movieItem['movie_id'] = rec_movie_id
            movieItem['movie_name'] = rec_movie_name
            yield movieItem

        # Save the recommendations in the database
        imdbItem = ImdbItem()
        imdbItem['movie_id'] = movie_id
        imdbItem['recommen_id'] = str(self.json_encoder.encode(recommen_ids))
        yield imdbItem

        # Save the state of the crawl till this point
        self.save_state()