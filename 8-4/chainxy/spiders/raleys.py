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

class raleys(scrapy.Spider):
	name = 'raleys'
	domain = ''
	history = []

	def start_requests(self):
		init_url = 'https://www.raleys.com/www/storelocator'	
		yield scrapy.Request(url=init_url, callback=self.body) 

	def body(self, response):
		print("=========  Checking.......")
		store_list = response.xpath('//div[@id="cms_content_frame"]//tr')
		for store in store_list[6:-1]:
			detail = self.eliminate_space(store.xpath('.//text()').extract())
			try:
				item = ChainItem()
				item['store_name'] = detail[0]
				item['address'] = ''
				item['city'] = ''
				addr = usaddress.parse(detail[1])
				for temp in addr:
					if temp[1] == 'PlaceName':
						item['city'] += temp[0].replace(',','')	+ ' '
					elif temp[1] == 'StateName':
						item['state'] = temp[0].replace(',','')
					elif temp[1] == 'ZipCode':
						item['zip_code'] = temp[0].replace(',','')
					else:
						item['address'] += temp[0].replace(',', '') + ' '
				item['country'] = 'United States'
				item['phone_number'] = self.validate(detail[2].split('Grocery Hours:')[0].strip()[1:-1])
				item['store_hours'] = self.validate(detail[2].split('Grocery Hours:')[1].strip())
				if item['store_name'] == 'Nob Hill Foods':
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