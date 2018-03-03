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

class cosbar(scrapy.Spider):
	name = 'cosbar'
	domain = ''
	history = []

	def start_requests(self):
		init_url = 'https://www.cosbar.com/store-locator/'
		header = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"Accept-Encoding":"gzip, deflate, sdch, br"
		}
		yield scrapy.Request(url=init_url, headers=header, callback=self.body) 

	def body(self, response):
		print("=========  Checking.......")
		data = response.body.split('var locations = ')[1].split('//	var states =')[0].strip()[:-1]
		store_list = json.loads(data)
		for store in store_list:
			try:
				item = ChainItem()
				item['store_name'] = self.validate(store['store_name'])
				item['address'] = self.validate(store['address'])
				item['city'] = self.validate(store['district'])
				item['state'] = self.validate(store['state'])
				item['zip_code'] = self.validate(store['postal_code'])
				item['country'] = self.validate(store['country'])
				item['phone_number'] = self.validate(store['store_phone'])
				item['latitude'] = self.validate(store['latitude'])
				item['longitude'] = self.validate(store['longitude'])
				yield item	
			except:
				passs

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