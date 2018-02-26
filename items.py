import scrapy


class RedditItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    subreddit = scrapy.Field()
    comments = scrapy.Field()
    rank = scrapy.Field()
    score = scrapy.Field()
    time = scrapy.Field()
    
