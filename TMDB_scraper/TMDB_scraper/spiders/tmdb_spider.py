# to run
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/8358-lie-to-me']
    
    
    def parse(self,response):
        
        cast=response.css("p.new_button a::attr(href)").get()
        cast_page="http://www.themoviedb.org"+cast
        
        yield scrapy.Request(cast_page, callback=self.parse_full_credits)
    
    
    def parse_full_credits(self,response):
        
        actors=response.css("ol.people.credits:not(.crew) a::attr(href)").getall()
        
        for actor in actors:
            actor_page="http://www.themoviedb.org"+actor
            
            yield scrapy.Request(actor_page, callback=self.parse_actor_page)
    
    
    def parse_actor_page(self,response):
        
        actor=response.css("h2.title a::text").get()
        
        movies=response.css("a.tooltip bdi::text").getall()
        # if need to be more specific: table.credit_group a.tooltip bdi::text
        
        for movie in movies:
            yield {
                "actor": actor,
                "movie_or_TV_name": movie
            }
        