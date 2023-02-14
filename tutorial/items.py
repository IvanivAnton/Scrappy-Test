# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class FilmCategory(Item):
    category_name = Field()
    items = Field()


class FilmCollection(Item):
    collection_name = Field()
    items = Field()


class FilmData(Item):
    film_name = Field()
    year = Field()
    rating = Field()
