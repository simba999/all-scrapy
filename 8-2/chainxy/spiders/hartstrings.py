from __future__ import unicode_literals
import scrapy
import json
import os
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem
from lxml import etree
from selenium import webdriver
from lxml import html
import usaddress

class hartstrings(scrapy.Spider):
	name = 'hartstrings'
	domain = ''
	history = []

	def start_requests(self):
		init_url = 'https://www.hourscenter.com/hartstrings/'
		yield scrapy.Request(url=init_url, callback=self.parse_city) 

	def parse_city(self, response):
		print("=========  Checking.......")
		city_list = response.xpath('//div[@class="states"]//ul[@class="state_list"]//a/@href').extract()
		for city in city_list:
			yield scrapy.Request(url=city, callback=self.parse_store)

	def parse_store(self, response):
		store_list = response.xpath('//ul[@class="listing_list"]//a/@href').extract()
		for store in store_list:
			yield scrapy.Request(url=store, callback=self.parse_page)

	def parse_page(self, response):
		try:
			item = ChainItem()
			item['address'] = self.validate(response.xpath('//span[@itemprop="streetAddress"]/text()').extract_first())
			item['city'] = self.validate(response.xpath('//span[@itemprop="addressLocality"]/text()').extract_first())
			item['state'] = self.validate(response.xpath('//span[@itemprop="addressRegion"]/text()').extract_first())
			item['zip_code'] = self.validate(response.xpath('//span[@itemprop="postalCode"]/text()').extract_first())
			item['country'] = 'United States'
			item['phone_number'] = self.validate(response.xpath('//li[@id="iphn"]//a/text()').extract_first())
			h_temp = ''
			hour_list = self.eliminate_space(response.xpath('//table[@class="hours_list"]//text()').extract())
			cnt = 1
			for hour in hour_list:
				if ':' in hour:
					h_temp += hour
					if cnt % 2 == 0:
						h_temp += ', '
					else:
						h_temp += ' '
					cnt += 1
			item['store_hours'] = h_temp[:-2]
			yield item
		except:
			pass	

	def validate(self, item):
		try:
			return item.strip()
		except:
			return ''

	def eliminate_space(self, items):
		tmp = []
		for item in items:
			if self.validate(item) != '':
				tmp.append(self.validate(item))
		return tmp

	def str_concat(self, items, unit):
		tmp = ''
		for item in items[:-1]:
			if self.validate(item) != '':
				tmp += self.validate(item) + unit
		tmp += self.validate(items[-1])
		return tmp