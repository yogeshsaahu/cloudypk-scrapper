from scrapy.spiders import CrawlSpider,Spider
import scrapy

class full_Cral(scrapy.Spider):
    name = "mycrawler"
    start_urls = [
        "http://cloudy.pk/",


    ]

    def start_requests(self):
      headers = {
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        }
      # meta = {"proxy": "http://20.242.203.179:3128"}
      for url in self.start_urls:
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)


    def parse(self, response):
       for item in response.css('h2.entry-title *::attr(href)'):

           yield response.follow(item.get(), callback=self.inside)

       next_page = response.css('a.next.page-numbers::attr(href)').get()
       if next_page is not None:
           yield response.follow(next_page, callback = self.parse)


    def inside(self, response):
        yield {
            'title': response.css("h1.entry-title *::text").get(),
            'image': response.css('img[width="200"]::attr(src)').get(),
            'storyline': response.css('p[style="text-align: center;"] *::text').get(),
            'download_links': response.css('a[style="font: 700 16px Open Sans; color: #fdfefe; background-color: #03a9f4; padding: 5px; text-transform: uppercase;"] *::attr(href)').getall(),
            'seo_description':response.css('meta[name="description"]::attr(content)').get().replace("Cloudy.pk","freemovies.gwaliorgeeks.com"),
            'seo_title': response.css('title::text').get().replace("Cloudy.pk","freemovies.gwaliorgeeks.com"),
        }




