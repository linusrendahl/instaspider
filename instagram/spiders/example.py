# -*- coding: utf-8 -*-
import scrapy
import re


class ExampleSpider(scrapy.Spider):
	name = 'example'
	start_urls = ['https://www.instagram.com/isabellalowengrip/']

	def parse(self, response):

		page = response.url.split("/")[-2]
		filename = 'instagram-%s-data.txt' % page

		with open(filename, 'w') as f:
			data = response.body.decode()
			text = re.search(r'window._sharedData = .*?};', data, re.DOTALL).group()
			f.write(text)
