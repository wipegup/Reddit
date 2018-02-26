import scrapy
from Reddit.items import RedditItem
from scrapy.selector import Selector

class RedditSpider(scrapy.Spider):
    name = 'RedditProj'
    allowed_domains = ['reddit.com']
    start_urls = [
    'https://www.reddit.com'
    ]

    def parse(self, response):
        items = []
        hxs = Selector(response)
        for sel in hxs.xpath('//div[contains(@class, "thing")]'):
            if sel.xpath("./text()").extract().find('submitted') != -1:
                item = RedditItem()
                item['title'] = sel.xpath("./a[@data-event-action = 'title'].text()").extract()
                item['subreddit'] = sel.xpath("./a[contains(@class, 'subreddit')].text()").extract()
                item['comments'] = sel.xpath("./@data-comments-count").extract()
                item['rank'] = sel.xpath("./@data-rank").extract()
                item['score'] = sel.xpath("./@data-score").extract()
                item['time'] = sel.xpath("./a[@class = 'tagline']./time[@class = 'live-timestamp'].text()").extract()

                items.append(item)

#//div[contains(@class, "thing")]/div/div/p/a[@data-event-action = "title"]

        return items
