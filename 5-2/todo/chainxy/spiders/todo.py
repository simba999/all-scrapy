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

class todo(scrapy.Spider):
	name = 'todo'
	domain = 'https://www.todo.com/'
	history = []

	def __init__(self):
		script_dir = os.path.dirname(__file__)
		file_path = script_dir + '/geo/cities.json'
		with open(file_path) as data_file:    
			self.location_list = json.load(data_file)

	def start_requests(self):
		header = {
			'Accept':'application/json, text/javascript, */*; q=0.01',
			'Accept-Encoding':'gzip, deflate, br',
			'Accept-Language':'en-US,en;q=0.8',
			'Connection':'keep-alive',
			'Content-Length':'0',
			'Content-Type':'application/json; charset=utf-8'
		}
		init_url  = ''
		yield scrapy.Request(url=init_url, headers=header, method="POST", callback=self.body) 

	def body(self, response):
		print("=========  Checking.......")
		with open('response.html', 'wb') as f:
			f.write(response.body)

		store_list = json.loads(response.body)
		for store in store_list:
			item = ChainItem()
			item['store_name'] = store['name']
			item['store_number'] = store['store_number']
			item['address'] = store['address']
			item['address2'] = store['crossStreet']
			item['city'] = store['city']
			item['state'] = store['state']
			item['zip_code'] = store['zip']
			item['country'] = store['country']
			item['phone_number'] = store['phone']
			item['latitude'] = store['latitude']
			item['longitude'] = store['longitude']
			item['store_hours'] = store['hours']
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