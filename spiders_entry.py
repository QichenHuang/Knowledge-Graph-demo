# -*- coding:utf-8 -*-

import argparse
import redis
import urls
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

CODE_MATCHER = {"SH": "shmb", "SZ300": "szcn", "SZ000": "szmb", "SZ002": "szsme"}
# 生成起始url并存储在redis服务器中
def generate_and_store_start_urls(host,codefile):
	# 创建redis连接实例
	pool = redis.ConnectionPool(host=host,port=6379,decode_responses=True)
	r = redis.Redis(connection_pool=pool)
	# 生成并存储公司的起始url
	company_urls = [urls.CFI_COMPANY % str(i) for i in range(1,74)]
	r.rpush('company:start_urls',*company_urls)
	# 生成通知信息和管理信息的起始url
	management_urls = []
	notice_urls = []
	with open(codefile) as f:
		for code in f:
			code = code.strip()
			notice_urls.append(urls.NOTICE_INFO_URL % code.lower())
			
			for sub in CODE_MATCHER:
				if sub in code:
					code = CODE_MATCHER[sub] + code[2:]
			management_urls.append(urls.CNINFO_MANAGEMENT % code)
	# 存储管理信息的起始url
	r.rpush('management:start_urls',*management_urls)
	
	# 存储通知信息的url
	r.rpush('notice:start_urls',*notice_urls)
	
# 运行爬虫		
def run_spider(spiders):
	process = CrawlerProcess(get_project_settings())
	for spider in spiders:
		process.crawl(spider)
	
	process.start()
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	
	parser.add_argument('--host',dest='host',default='localhost',help='Redis服务器地址，默认为本地localhost')
	parser.add_argument('--codefile',dest='codefile',default='medicine_company_list.txt',help='公司代码列表，默认为 medicine_company_list.txt ')
	parser.add_argument('--master',dest='master',default='1',help='是master还是slave，1 表示master，0 表示slave，默认为 1 ')
	parser.add_argument('--spiders',dest='spiders',default='companySpider,managementSpider,noticeSpider',help='选择爬虫，用逗号分隔，默认为 companySpider,managementSpider,noticeSpider ')
	
	args = parser.parse_args()
	# print(args.host)
	# print(args.codefile)
	# print(args.master)
	# print(args.spiders)
	if args.master == '1':
		generate_and_store_start_urls(args.host,args.codefile)
	run_spider(args.spiders.split(','))

	