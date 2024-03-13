import scrapy


class FmylifeSpider(scrapy.Spider):
    name = 'fmylife'
    allowed_domains = ['fmylife.com']
    start_urls = ['https://www.fmylife.com/']

    def parse(self, response):
        for post in response.css("div.panel-content"):
        	yield {
               'upvote' : post.css("button.btn.btn-default.vote-up.title::text").extract(),
               'downvote' : post.css("button.btn.btn-default.vote-down.title::text").extract(),
               'comments': post.css("a.bullecomment.animateNumber::text").extract() ,
               'post' : post.css("a::text").extract(),
        	}
        	
            # follow pagination
        next_page_url = response.css('a.jscroll-next.btn.btn-primary.btn-lg::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
 
