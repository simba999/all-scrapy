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
import pdb

class audiology(scrapy.Spider):
	name = 'audiology'
	domain = ''
	history = []

	def __init__(self):
		self.driver = webdriver.Chrome("./chromedriver")
		script_dir = os.path.dirname(__file__)

	def start_requests(self):
		init_url = 'http://memberportal.audiology.org'
		yield scrapy.Request(url=init_url, callback=self.body)
	
	def body(self, response):
		self.driver.get("http://memberportal.audiology.org/Directories/Find-an-Audiologist?protected=true")
		self.driver.find_element_by_id('dnn_ctr2708_Find_ctl00_uscSearchForm_pnlFields_i0_i0_rcbLeft_Input').send_keys('U')
		self.driver.find_element_by_id('dnn_ctr2708_Find_ctl00_btnSearch').click()
		self.driver.find_element_by_id('dnn_ctr2708_Find_ctl00_ListPagerControl_lnkNext').click()
		pdb.set_trace()
		# source = self.driver.page_source.encode("utf8")
		# tree = etree.HTML(source)
		# store_list = tree.xpath('//section//div[contains(@class, "stores")]//a[2]/@href')
		# for store in store_list:
		# 	yield scrapy.Request(url=store, callback=self.parse_page)

	def parse_page(self, response):
		try:
			item = ChainItem()
			detail = self.eliminate_space(response.xpath('//div[contains(@class, "address")]//text()').extract())
			item['store_name'] = ''
			item['store_number'] = ''
			item['address'] = self.validate(detail[0])
			addr = detail[1].split(',')
			item['city'] = self.validate(addr[0].strip())
			sz = addr[1].strip().split(' ')
			item['state'] = ''
			item['zip_code'] = self.validate(sz[len(sz)-1])
			for temp in sz[:-1]:
				item['state'] += self.validate(temp) + ' '
			item['phone_number'] = detail[2]
			item['country'] = 'United States'
			h_temp = ''
			hour_list = self.eliminate_space(response.xpath('//div[contains(@class, "hours")]//text()').extract())
			cnt = 1
			for hour in hour_list:
				h_temp += hour
				if cnt % 2 == 0:
					h_temp += ', '
				else:
					h_temp += ' '
				cnt += 1
			item['store_hours'] = h_temp[:-2]
			yield item	
		except:
			pdb.set_trace()		

	def validate(self, item):
		try:
			return item.strip()
		except:
			return ''

	def eliminate_space(self, items):
		tmp = []
		for item in items:
			if self.validate(item) != '' and 'STORE HOURS:' not in self.validate(item):
				tmp.append(self.validate(item))
		return tmp
