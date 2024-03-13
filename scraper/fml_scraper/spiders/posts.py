from pathlib import Path

import scrapy


class PostSpider(scrapy.Spider):
    name = "posts"
    start_urls = ["https://www.fmylife.com/"]
    base_url = "https://www.fmylife.com/?page="
    page_number = 1


    def parse(self, response):
        posts = response.css("article.bg-white")
        for post in posts:
            title = post.xpath(".//h2/a/text()").get()
            meta = post.xpath(".//p/text()").getall()
            gender = post.xpath(".//i/@class").extract()
            body = post.xpath(".//a[contains(@class, 'block text-blue-500 dark:text-white my-4')]/text()").get()
            agree = post.xpath(".//div[contains(@class, 'flex vote-type-0')]//span[contains(@class, 'vote-btn-count')]/text()").get()
            deserved = post.xpath(".//div[contains(@class, 'flex vote-type-1')]//span[contains(@class, 'vote-btn-count')]/text()").get()


            yield {
                'title': title,
                'meta': meta,
                'gender': gender,
                'body': body,
                'agree': agree,
                'deserved': deserved
            }
        self.page_number += 1
        next_page_url = self.base_url + str(self.page_number)

        yield scrapy.Request(next_page_url)