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
        regions = response.xpath('//table/tbody/tr/td[@class="views-field views-field-field-region"]/a/text()').extract()
        local_events = response.xpath('//table/tbody/tr/td[@class="views-field views-field-field-event-location"]/a/text()').extract()
        project_names = response.xpath('//table/tbody/tr/td[@class="views-field views-field-title active"]/a/text()').extract()
        team_names = [s.strip() for s in response.xpath('//table/tbody/tr/td[@class="views-field views-field-field-team-name"]/text()').extract() if s.strip() != ""]
        for i in range(len(team_names)):
            item['region'] = regions[i]
            item['local_event'] = local_events[i]
            item['project_name'] = project_names[i]
            item['team_name'] = team_names[i]
            yield item

        for href in response.xpath('//table/tbody/tr/td[@class="views-field views-field-title active"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)
            
    def parse_dir_contents(self, response):
        item = GovhackItem() 
        item['project_name'] = response.xpath('//div/div/section/h1[@class="page-header"]/text()').extract()
        item['prizes'] = response.xpath('//body/div/div/section/div/section/article/div[@class="field field-name-field-prizes field-type-entityreference field-label-above"]/div/div/a/text()').extract()
        yield item
            
