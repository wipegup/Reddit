import scrapy
from Reddit.items import RedditItem
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time
class RedditSpider(CrawlSpider):
    name = 'RedditProj'
    allowed_domains = ['reddit.com']
    start_urls = [
    'https://www.reddit.com'
    ]

    rules = (
        #Rule(LinkExtractor(allow = ('^https://www.reddit.com$'), deny = ('www.reddit.com/[a-z]')), callback = 'parse_item'),
        Rule(
        LinkExtractor(allow=('\?count=\d+&after', ),
        deny = ('\?count=500')), follow = True, callback = 'parse_item' ),
    )

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        items = []
        hxs = Selector(response)
        for sel in hxs.xpath('//div[contains(@class, "thing")]'):
            if sel.xpath(".//p[contains(@class, 'tagline')]/text()").extract()[0].find('submitted')!=-1:
                item = RedditItem()
                item['title'] = sel.xpath(".//a[@data-event-action = 'title']/text()").extract()
                item['subreddit'] = sel.xpath(".//a[contains(@class, 'subreddit')]/text()").extract()
                item['comments'] = sel.xpath("./@data-comments-count").extract()
                item['rank'] = sel.xpath("./@data-rank").extract()
                item['score'] = sel.xpath("./@data-score").extract()
                item['timePosted'] = sel.xpath(".//p[contains(@class, 'tagline')]/time/@title").extract()
                item['timeScraped'] = time.time()
                #item['liveScore'] = sel.xpath(".//div[@class = 'score unvoted']/text()").extract()
                item['liveComments'] = sel.xpath(".//a[@data-event-action = 'comments']/text()").extract()

                items.append(item)
            else:
                print('no')

#//div[contains(@class, "thing")]/div/div/p/a[@data-event-action = "title"]

        return items
class BigRedditSpider(CrawlSpider):
    name = 'RedditProjBig'
    allowed_domains = ['reddit.com']
    start_urls = [
    'https://www.reddit.com'
    ]

    rules = (
        #Rule(LinkExtractor(allow = ('^https://www.reddit.com$'), deny = ('www.reddit.com/[a-z]')), callback = 'parse_item'),
        Rule(
        LinkExtractor(allow=('\?count=\d+&after', ),
        ), follow = True, callback = 'parse_item' ),
    )

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        items = []
        hxs = Selector(response)
        for sel in hxs.xpath('//div[contains(@class, "thing")]'):
            if sel.xpath(".//p[contains(@class, 'tagline')]/text()").extract()[0].find('submitted')!=-1:
                item = RedditItem()
                item['title'] = sel.xpath(".//a[@data-event-action = 'title']/text()").extract()
                item['subreddit'] = sel.xpath(".//a[contains(@class, 'subreddit')]/text()").extract()
                item['comments'] = sel.xpath("./@data-comments-count").extract()
                item['rank'] = sel.xpath("./@data-rank").extract()
                item['score'] = sel.xpath("./@data-score").extract()
                item['timePosted'] = sel.xpath(".//p[contains(@class, 'tagline')]/time/@title").extract()
                item['timeScraped'] = time.time()
                #item['liveScore'] = sel.xpath(".//div[@class = 'score unvoted']/text()").extract()
                item['liveComments'] = sel.xpath(".//a[@data-event-action = 'comments']/text()").extract()

                items.append(item)
            else:
                print('no')

#//div[contains(@class, "thing")]/div/div/p/a[@data-event-action = "title"]

        return items

# To Run scrapy crawl RedditProj -o RedditFeb.16.1730.csv -t csv
