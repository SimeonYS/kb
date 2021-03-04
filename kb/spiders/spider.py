import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import KbItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class KbSpider(scrapy.Spider):
	name = 'kb'
	start_urls = ['https://www.kb.cz/en/about-the-bank/for-media']

	def parse(self, response):
		post_links = response.xpath('//div[@class="col-md-6 col-lg-4"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//h2[@class="article__date montserat-black col-12 col-md-3"]/text()').get().strip()
		title = ' '.join([response.xpath('//h1[@class="page-header__title montserat-black"]/text()').get() + response.xpath('//span[@class="page-header__subtitle opensans"]/text()').get()])
		content = response.xpath('//div[contains(@class,"article grey-version")]//text()[not (ancestor::h2)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=KbItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
