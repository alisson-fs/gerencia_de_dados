import scrapy
import json


class MercadoLivre(scrapy.Spider):
    name = "mercado_livre"

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 10,
    }

    def start_requests(self):
        for page in range(1, 10000, 50):
            yield scrapy.Request(
                f"https://lista.mercadolivre.com.br/celulares-telefones/celulares-smartphones/iphone/iphone_Desde_{page}_NoIndex_True"
            )

    def parse(self, response, **kwargs):
        items = response.css(".ui-search-layout__item")
        for item in items:
            yield {
                "title": item.css(".ui-search-item__title::text").get(),
                "price": item.css(".andes-money-amount__fraction::text").get(),
                "reviews_rating": item.css(
                    ".ui-search-reviews__rating-number::text"
                ).get(),
                "reviews_amount": item.css(".ui-search-reviews__amount::text").get(),
                "store_label": item.css(".ui-search-official-store-label::text").get(),
                "price-discount": item.css(".ui-search-price__discount::text").get(),
                "free-shipping": item.css(".ui-pb-highlight::text").get()
                == "Frete grátis",
                "item-variations": item.css(
                    ".ui-search-item__variations-text::text"
                ).get(),
            }
