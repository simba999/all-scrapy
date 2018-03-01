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

class murphyusa(scrapy.Spider):
	name = 'murphyusa'
	domain = ''
	history = []

	def __init__(self, *args, **kwargs):
		script_dir = os.path.dirname(__file__)
		file_path = script_dir + '/geo/US_Cities.json'
		with open(file_path) as data_file:    
			self.location_list = json.load(data_file)
		file_path = script_dir + '/geo/US_CA_States.json'
		with open(file_path) as data_file:    
			self.US_CA_States_list = json.load(data_file)

	def start_requests(self):
		init_url = 'http://locator.murphyusa.com/MapServices.asmx/GetLocationsByRadius'
		header={
			"Accept":"*/*",
			"Accept-Encoding":"gzip, deflate",
			"Content-Type":"application/json; charset=UTF-8",
			"X-Requested-With":"XMLHttpRequest"
		}
		for location in self.location_list:
			payload={
				"filter": "",
				"lat":str(location['latitude']),
				"lng":str(location['longitude']),
				"searchRadius":"500"
			}
			yield scrapy.Request(url=init_url, headers=header, body=json.dumps(payload), method='post', callback=self.body) 

	def body(self, response):
		print("=========  Checking.......")
		store_list = json.loads(response.body)['d']
		for store in store_list:
			try:
				item = ChainItem()
				item['store_name'] = 'Murphy'
				item['store_number'] = self.validate(str(store['StoreNum']))
				item['address'] = self.validate(store['Address'])				
				item['city'] = self.validate(store['City'])
				item['state'] = self.validate(store['State'])
				item['zip_code'] = self.validate(store['Zip'])
				item['country'] = 'United States'
				item['phone_number'] = self.validate(store['Phone'])
				item['latitude'] = self.validate(str(store['Lat']))
				item['longitude'] = self.validate(str(store['Long']))
				if item['store_number'] not in self.history:
					self.history.append(item['store_number'])
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