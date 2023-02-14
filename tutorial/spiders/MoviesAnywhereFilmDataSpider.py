import json

import scrapy
from scrapy.loader import ItemLoader

from tutorial.items import FilmData


class MoviesAnywhereFilmDataSpider(scrapy.Spider):
    name = 'movies-anywhere-film-data'

    custom_settings = {
        'FEED_URI': 'new-releases-film-data.jsonl',
        'FEED_FORMAT': 'jsonl'
    }

    def start_requests(self):
        movies = open('movies.jsonl', 'r')
        lines = movies.readlines()
        new_releases = {
            'items': []
        }
        for line in lines:
            new_releases = json.loads(line.strip())
            break

        films = new_releases['items']

        for film in films:
            yield scrapy.Request(url="https://moviesanywhere.com" + film['link'])

    def parse(self, response, **kwargs):
        loader = ItemLoader(item=FilmData(), response=response)
        film_name = response.xpath('/html/head/title/text()').get().split('|')[0][:-1]
        loader.add_value('film_name', film_name)
        loader.add_xpath('year', '//main/div/div[3]/div[2]/div[1]/div[2]/div/ul/li[3]/span/span/text()')
        loader.add_xpath('rating', '//main/div/div[3]/div[2]/div[1]/div[2]/div/div/div/div/span/text()')
        yield loader.load_item()
