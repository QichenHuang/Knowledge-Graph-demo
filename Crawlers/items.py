# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Info_Item(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	info = scrapy.Field()

class CompanyItem(scrapy.Item):
	code = scrapy.Field()
	securities_abbreviation = scrapy.Field()
	name = scrapy.Field()
	address = scrapy.Field()
	zipcode = scrapy.Field()
	register_address = scrapy.Field()
	register_number = scrapy.Field()
	representative = scrapy.Field()
	manager = scrapy.Field()
	
class ManagementItem(scrapy.Item):
	name = scrapy.Field()
	post = scrapy.Field()
	year_of_born = scrapy.Field()
	sex = scrapy.Field()
	education = scrapy.Field()
	company_code = scrapy.Field()
	
class NoticeItem(scrapy.Item):
	title = scrapy.Field()
	type = scrapy.Field()
	date = scrapy.Field()
	url = scrapy.Field()
	company_code = scrapy.Field()
	content = scrapy.Field()
	source = scrapy.Field()