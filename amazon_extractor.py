import scrapy
import json
import random


class Amazon(scrapy.Spider):
    name = "amazon"

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
    ]

    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 10,
        "AUTOTHROTTLE_MAX_DELAY": 60,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        "DOWNLOAD_DELAY": 5,
        "RETRY_TIMES": 10,
        "USER_AGENT": random.choice(user_agents),
    }

    def start_requests(self):
        for page in range(1, 100):
            yield scrapy.Request(f"https://www.amazon.com.br/s?k=iphone&page={page}")

    def parse(self, response, **kwargs):
        items = response.xpath('//div[contains(@class, "s-result-item")]')
        for item in items:
            yield {
                "title": item.xpath(
                    './/span[@class="a-size-base-plus a-color-base a-text-normal"]/text()'
                ).get(),
                "price": item.xpath('.//span[@class="a-price-whole"]/text()').get(),
                "reviews_rating": item.xpath(
                    './/span[@class="a-icon-alt"]/text()'
                ).get(),
                "reviews_amount": item.xpath(
                    './/span[@class="a-size-base s-underline-text"]/text()'
                ).get(),
                "store_label": None,
                "price_discount": item.xpath(
                    './/span[@class="a-price a-text-price"]/text()'
                ).get(),
                "free_shipping": bool(
                    item.xpath(
                        './/span[contains(text(), "frete GRÁTIS disponível")]'
                    ).get()
                ),
                "item_variations": item.xpath(
                    './/span[@class="a-truncate-cut"]/text()'
                ).get(),
            }
