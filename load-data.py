import re
import scrapy
from scrapy.crawler import CrawlerProcess
import os


class InstaSpider(scrapy.Spider):
	name = 'example'
	start_urls = []
	username = ''

	def __init__(self):
		self.username = input('Who do you want to crawl?')
		self.start_urls = ['https://www.instagram.com/'+self.username+'/']
		# Google cache URL: 'http://webcache.googleusercontent.com/search?q=cache:instagram.com/'+username+'/&num=1&strip=0&vwsrc=1'

	def parse(self, response):

		page = response.url.split("/")[-2]
		filename = 'instagram-%s-data.txt' % page
		path = 'data/json/'

		with open(os.path.join(path, filename), 'w') as f:
			data = response.body.decode()
			text = re.search(r'window._sharedData = .*?};', data, re.DOTALL).group()
			f.write(text)


class LoadData():

	def open(self, username):
		filename = 'instagram-%s-data.txt' % username
		path_json = 'data/json/'
		path_html = 'data/html/'

		with open(os.path.join(path_json, filename), 'r') as f, open('data-viewer.htm', 'r') as source, open(os.path.join(path_html, 'data-viewer-'+username+'.htm'), 'w') as outfile:
			data = f.read()

			html = source.read()
			newhtml = re.sub('{{ data }}', data, html)
			
			newhtml = newhtml.replace('\n', ' ').replace('\r', '')

			outfile.write(newhtml)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})


username = input('Load data for user: ')

process.crawl(InstaSpider)
process.start()

Loader = LoadData()
Loader.open(username)