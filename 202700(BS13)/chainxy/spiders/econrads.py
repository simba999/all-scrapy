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

class econrads(scrapy.Spider):
	name = 'econrads'
	domain = 'https://www.econrads.com/'
	history = []

	def start_requests(self):
		init_url = 'https://www.econrads.com/Car-Services-Store-Locator.aspx'
		yield scrapy.Request(url=init_url, callback=self.body) 

	def body(self, response):
		print("=========  Checking.......")
		store_list = response.xpath('//div[@class="sidemenu"]//a/@href').extract()
		for store in store_list:
			store = self.domain + store
			yield scrapy.Request(url=store, callback=self.parse_page)

	def parse_page(self, response):
		try:
			item = ChainItem()
			item['store_name'] = self.validate(response.xpath('//span[@id="ctl00_ctl00_ContentSection_ContentSection_lblLocationName"]/text()').extract_first())
			item['address'] = self.validate(response.xpath('//span[@id="ctl00_ctl00_ContentSection_ContentSection_lblAddress1"]/text()').extract_first())
			item['address2'] = self.validate(response.xpath('//span[@id="ctl00_ctl00_ContentSection_ContentSection_lblAddress2"]/text()').extract_first())
			address = self.validate(response.xpath('//span[@id="ctl00_ctl00_ContentSection_ContentSection_lblCity"]/text()').extract_first())
			addr = address.split(',')
			item['city'] = self.validate(addr[0].strip())
			item['state'] = self.validate(addr[1].strip().split(' ')[0].strip())
			item['zip_code'] = self.validate(addr[1].strip().split(' ')[1].strip())
			item['country'] = 'United States'
			item['phone_number'] = self.validate(response.xpath('//span[@id="ctl00_ctl00_ContentSection_ContentSection_lblPhone"]/text()').extract_first())
			h_temp = ''
			hour_list = self.eliminate_space(response.xpath('//span[@id="ctl00_ctl00_ContentSection_ContentSection_lblHoursOfOperation"]//text()').extract())
			cnt = 1
			for hour in hour_list:
				h_temp += hour + ', '
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