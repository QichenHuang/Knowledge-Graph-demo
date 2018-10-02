# -*- coding:utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from Crawlers.items import Info_Item
from Crawlers.items import CompanyItem
from Crawlers.items import ManagementItem
from Crawlers.items import NoticeItem
import re
import scrapy
from functools import reduce

CODE_MATCHER = {"shmb": "SH", "szcn": "SZ", "szmb": "SZ", "szsme": "SZ"}
COMPANY_HEADER = {'代码':'code','证券简称':'securities_abbreviation','公司名称':'name','公司注册地址':'address',\
	'公司注册地址邮箱':'zipcode','首次注册登记地点':'register_address','企业法人营业执照注册号':'register_number',\
	'法人代表':'representative','总经理':'manager'}
MANAGEMENT_HEADER = {'姓名':'name','职务':'post','出生年份':'year_of_born','性别':'sex','学历':'education'}

class CompanySpider(RedisSpider):
	name = 'companySpider'
	redis_key = 'company:start_urls'
	
	def parse(self,response):
		#print('---------------------重要的信息来了————————————————————————')
		# 得到表头
		rows = response.xpath('//table[@class="table_data"]//tr')
		header = rows[0].xpath('td//text()').extract()
		header = list(map(lambda x:COMPANY_HEADER[x],header))
		# 循环得到每一行内容，生成item存储
		items = []
		for row in rows[1:]:
			content = row.xpath('td//text()').extract()
			item = CompanyItem()
			item.update(dict(zip(header,content)))
			items.append(item)
		return items
	
class NoticeSpider(RedisSpider):
	name = 'noticeSpider'
	redis_key = 'notice:start_urls'
	
	def parse(self,response):
		# print('---------------------重要的信息来了————————————————————————')
		code = re.match(r'.+=([\w]+)',response.url).group(1).upper()
		rows = response.xpath('//table[@class="body_table"]/tbody/tr')
		for row in rows:
			info = {}
			info['title'] = row.xpath('th/a/text()').extract_first()
			info['type'],info['date'] = row.xpath('td/text()').extract()
			info['url'] = row.xpath('th/a/@href').extract_first()
			info['company_code'] = code
			yield response.follow(info['url'],meta={'info':info},callback=self.notice_parse)
		'''info = {}
		info['title'] = rows[0].xpath('th/a/text()').extract_first()
		info['type'],info['date'] = rows[0].xpath('td/text()').extract()
		info['url'] = rows[0].xpath('th/a/@href').extract_first()
		info['code'] = code
		# yield response.follow(info['url'],meta={'info':info},callback=self.notice_parse)
		info['url'] = response.urljoin(info['url'])
		yield scrapy.Request(info['url'],callback=self.notice_parse)'''
	
	def notice_parse(self,response):
		content = response.xpath('//div[@id="content"]/p/text()').extract()
		if content:
			content = reduce(lambda x,y:x+'\n'+y,content)
			meta = response.meta['info']
			meta['content']=content
			meta['source']='公告'
			item = NoticeItem()
			item.update(meta)
			return item
	
	
class ManagementSpider(RedisSpider):
	name = 'managementSpider'
	redis_key = 'management:start_urls'
	
	def parse(self,response):
		# 计算得到当前公司的代码
		code = re.match(r'.*/(\w*?)\.html',response.url).group(1)
		for key in CODE_MATCHER:
			if key in code:
				code = code.replace(key,CODE_MATCHER[key])
		# 得到表头
		rows = response.xpath('//div[@class="clear"]/table/tr')
		header = rows[0].xpath('td//text()').extract()
		header = list(map(lambda x:MANAGEMENT_HEADER[x],header))
		header.append('company_code')
		# 循环得到每一行内容，生成item存储
		items = []
		for row in rows[1:]:
			content = row.xpath('td//text()').extract()
			content = list(map(lambda x:x.strip(),content))
			content.append(code)
			item = ManagementItem()
			item.update(dict(zip(header,content)))
			items.append(item)
		return items