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
import pdb

class holidayinnexpress(scrapy.Spider):
	name = 'holidayinnexpress'
	domain = ''
	history = []
	
	def start_requests(self):
		init_url  = 'https://www.ihg.com/holidayinnexpress/destinations/us/en/united-states-hotels'
		yield scrapy.Request(url=init_url, callback=self.parse_state) 

	def parse_state(self, response):
		state_list = response.xpath('//li[@class="listingItem"]//a/@href').extract()
		for state in state_list : 
			# if 'https://www.ihg.com/holidayinnexpress/holidayinnexpress/hotels/us/en/customer-care/interstitial?destUrl=https%3A%2F%2Fwww.kimptonhotels.com%3Farrive%3D07%2F15%2F2017%26child%3D0%26depart%3D07%2F16%2F2017%26adult%3D1%26src%3Dihg.com%26hotel%3D74903' in state:
			# 	print('~~~~~~~~~~~~~~~~~ parse_state level')
			# 	pdb.set_trace()
			yield scrapy.Request(url=state, callback=self.parse_city)

	def parse_city(self, response):
		city_list = response.xpath('//li[@class="listingItem"]//a/@href').extract()
		for city in city_list :
			# if 'https://www.ihg.com/holidayinnexpress/holidayinnexpress/hotels/us/en/customer-care/interstitial?destUrl=https%3A%2F%2Fwww.kimptonhotels.com%3Farrive%3D07%2F15%2F2017%26child%3D0%26depart%3D07%2F16%2F2017%26adult%3D1%26src%3Dihg.com%26hotel%3D74903' in city:
			# 	print('~~~~~~~~~~~~~~~~~ parse_state level')
			# 	pdb.set_trace()
			yield scrapy.Request(url=city, callback=self.parse_store)
	
	def parse_store(self, response):
		store_list = response.xpath('//div[@class="row top_hotelName sl_whiteout"]//a/@href').extract()
		for store in store_list:
			# if 'https://www.ihg.com/holidayinnexpress/holidayinnexpress/hotels/us/en/customer-care/interstitial?destUrl=https%3A%2F%2Fwww.kimptonhotels.com%3Farrive%3D07%2F15%2F2017%26child%3D0%26depart%3D07%2F16%2F2017%26adult%3D1%26src%3Dihg.com%26hotel%3D74903' in store:
			# 	print('~~~~~~~~~~~~~~~~~ parse_state level')
			# 	pdb.set_trace()
			try:
				yield scrapy.Request(url=store, callback=self.parse_page)
			except:
				pass

	def parse_page(self, response):
		pass
		# try:
		# 	item = ChainItem()
		# 	item['address'] = self.validate(response.xpath('//span[@itemprop="streetAddress"]//p/text()').extract_first())
		# 	item['city'] = self.validate(response.xpath('//span[@itemprop="addressLocality"]/text()').extract_first())
		# 	item['state'] = self.validate(response.xpath('//span[@itemprop="addressRegion"]/text()').extract_first())
		# 	item['zip_code'] = self.validate(response.xpath('//span[@itemprop="postalCode"]/text()').extract_first())
		# 	item['country'] = 'United States'
		# 	item['phone_number'] = self.validate(response.xpath('//span[@itemprop="telephone"]/text()').extract_first())
		# 	item['latitude'] = self.validate(response.xpath('//meta[@itemprop="latitude"]/@content').extract_first())
		# 	item['longitude'] = self.validate(response.xpath('//meta[@itemprop="longitude"]/@content').extract_first())
		# 	if item['address'] == '':
		# 		item['address'] = self.validate(response.xpath('//span[@itemprop="streetAddress"]/text()').extract_first())
		# 		item['city'] = self.validate(response.xpath('//span[@itemprop="addressLocality"]/text()').extract_first())
		# 		item['state'] = self.validate(response.xpath('//span[@itemprop="addressRegion"]/text()').extract_first()).split(' ')[0]
		# 		item['zip_code'] = self.validate(response.xpath('//span[@itemprop="addressRegion"]/text()').extract_first()).split(' ')[1]
		# 	yield item			
		# except:
		# 	pass

	def eliminate_space(self, items):
		tmp = []
		for item in items:
			if self.validate(item) != '':
				tmp.append(self.validate(item))
		return tmp

	def validate(self, item):
		try:
			return item.encode('raw-unicode-escape').replace('\xa0', '').strip().replace(',','')
		except:
			return ''

	def check_country(self, item):
		for state in self.US_CA_States_list:
			if item.lower() in state['abbreviation'].lower():
				return state['country']
		return ''