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

class countrystyle(scrapy.Spider):
	name = 'countrystyle'
	domain = 'https://www.countrystyle.com/'
	history = ['']

	def start_requests(self):
		init_url  = 'https://www.countrystyle.com/wp-content/themes/CS/locator/data/cs_locations.json'
		yield scrapy.Request(url=init_url, callback=self.body) 

	def body(self, response):
		print("=========  Checking.......")
		store_list = json.loads(response.body)
		for store in store_list:
			item = ChainItem()
			item['store_name'] = ''
			item['store_number'] = store['store_id']
			item['address'] = store['address']
			item['address2'] = store['address_2']
			item['city'] = store['city']
			item['state'] = store['state']
			item['zip_code'] = store['zip']
			item['country'] = 'Canada'
			item['phone_number'] = store['phone']
			item['latitude'] = store['lat']
			item['longitude'] = store['lng']
			item['store_hours'] = ''
			item['store_type'] = ''
			item['other_fields'] = ''
			item['coming_soon'] = ''
			if item['store_number'] in self.history:
				continue
			self.history.append(item['store_number'])
			yield item	

	def validate(self, item):
		try:
			return item.strip()
		except:
			return ''