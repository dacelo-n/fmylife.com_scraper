from pathlib import Path

import scrapy


class PostSpider(scrapy.Spider):
    name = "posts"
    start_urls = [
        "https://www.fmylife.com/",   
    ]
    base_url = "https://www.fmylife.com/?page="
    page_number = 1



    def parse(self, response):
        # Extracting FML posts
        posts = response.css("article.bg-white")
        for post in posts:
            title = post.xpath('.//h2/a/text()').get()
            body = post.xpath('.//a[contains(@class, "text-blue-500")]/text()').get()
            agree, deserve = post.xpath('.//div[contains(@class, "flex-wrap")]//span[contains(@class, "w-20")]/text()').getall()


            yield {
                'title': title,
                'body': body,
                'agree': agree,
                'deserve': deserve
            }
        self.page_number += 1
        next_page_url = self.base_url + str(self.page_number)

        yield scrapy.Request(next_page_url)