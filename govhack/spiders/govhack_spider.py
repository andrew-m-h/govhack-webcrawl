import scrapy

from govhack.items import GovhackItem

class GovhackSpider(scrapy.Spider):
    name = 'govhack'
    allowed_domains = ['2016.hackerspace.govhack.org']
    start_urls = [
        "https://2016.hackerspace.govhack.org/projects/"
    ]
    
    def parse(self, response):
        item = GovhackItem()
        item['region']       = response.xpath('//table/tbody/tr/td[@class="views-field views-field-field-region"]/a/text()').extract()
        item['local_event']  = response.xpath('//table/tbody/tr/td[@class="views-field views-field-field-event-location"]/a/text()').extract()
        item['project_name'] = response.xpath('//table/tbody/tr/td[@class="views-field views-field-title active"]/a/text()').extract()
        item['team_name']    = [s.strip() for s in response.xpath('//table/tbody/tr/td[@class="views-field views-field-field-team-name"]/text()').extract() if s.strip() != ""]
        yield item

        for href in response.xpath('//table/tbody/tr/td[@class="views-field views-field-title active"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)
            
    def parse_dir_contents(self, response):
        item = GovhackItem()
        item['prizes'] = response.xpath('//body/div/div/section/div/section/article/div[@class="field field-name-field-prizes field-type-entityreference field-label-above"]/div/div/a/text()').extract()
        yield item
            
