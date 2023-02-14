import scrapy
from scrapy.loader import ItemLoader

from tutorial.items import FilmCollection, FilmCategory


class MoviesAnywhereExploreSpider(scrapy.Spider):
    name = 'movies-anywhere'

    custom_settings = {
        'FEED_URI': 'movies.jsonl',
        'FEED_FORMAT': 'jsonl'
    }

    def start_requests(self):
        urls = [
            'https://moviesanywhere.com/explore'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        slider_blocks_ids = response.xpath('//main/div/div/@id').getall()
        for block_id in slider_blocks_ids:
            blocks_with_sliders = response.css('main div div#' + block_id)

            category_name = blocks_with_sliders.xpath('./div/h2/text()').get()

            if category_name:
                yield from self.parse_film_category(block=blocks_with_sliders)
            else:
                yield from self.parse_film_collections(block=blocks_with_sliders)

    @staticmethod
    def parse_film_category(block):
        category_name = block.xpath('./div/h2/text()').get()
        loader = ItemLoader(item=FilmCategory(), response=block)
        loader.add_value('category_name', category_name)

        films = block.css('.slick-slide')
        items = []
        for film_item in films:
            category_item = {
                'name': film_item.css('div div div a div:first-child span::text').get(),
                'link': film_item.xpath('./div/div/div/a/@href').get(),
            }
            if category_item['name'] and category_item['link']:
                items.append(category_item)

        loader.add_value('items', items)
        yield loader.load_item()

    @staticmethod
    def parse_film_collections(block):
        collection_name = block.xpath('./h2/text()').get()
        loader = ItemLoader(item=FilmCollection(), response=block)
        loader.add_value('collection_name', collection_name)

        collections = block.css('.slick-slide')
        items = []
        for collection in collections:
            collection_item = {
                'name': collection.xpath('./div/div/a/div/span/text()').get(),
                'link': collection.xpath('./div/div/a/@href').get(),
            }
            if collection_item['name'] and collection_item['link']:
                items.append(collection_item)

        loader.add_value('items', items)
        yield loader.load_item()
