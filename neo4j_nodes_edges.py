# -*- coding:utf-8 -*-

import redis
import json
import csv

# 从redis服务其中读取特定key的内容，参数r表示redis的连接实例，返回list of dict或者None
def read_from_redis(r,key):
	if not r.exists(key):
		print('key:%s 不存在！！' % key)
		return None
	items = r.lrange(key,0,-1)
	items = list(map(json.loads,items))
	return items
# 将company信息以neo4j可导入的格式写入csv文件中
def company_nodes_file(r,key,filename):
	items = read_from_redis(r,key)
	if not items:
		return
	company_properties = list(items[0].keys())
	company_header = [':ID',':LABEL'] + company_properties
	with open(filename,'w',newline='') as file:
		writer = csv.writer(file)
		writer.writerow(company_header)
		for item in items:
			company_data = ['comp%s'%item['code'],'Company'] + list(map(lambda x:item[x],company_properties))
			writer.writerow(company_data)
# 从management：items的信息中提取出个人信息和职位信息		
def person_and_management(r,key):
	items = read_from_redis(r,key)
	if not items:
		return None
	person_properties = ['name','year_of_born','sex','education']
	person_header = [':ID',':LABEL'] + person_properties
	management_header = [':START_ID',':END_ID',':TYPE','post']
	person = [person_header]
	management = [management_header]
	for index,item in enumerate(items):
		person_ID = 'per%d' % index
		company_ID = 'comp%s' % (item['company_code'][-6:])
		
		person.append([person_ID,'Person'] + list(map(lambda x:item[x],person_properties)))
		posts = item['post'].split(',')
		for post in posts:
			management.append([company_ID, 'per%d'%index,'isManagedBy',post])
	return person,management
# 将person信息写入文件
def person_nodes_file(person,filename):
	with open(filename,'w',newline='') as file:
		writer = csv.writer(file)
		writer.writerows(person)
	
# 将management信息写入文件
def management_edges_file(management,filename):
	with open(filename,'w',newline='') as file:
		writer = csv.writer(file)
		writer.writerows(management)
	
if __name__=='__main__':
	pool = redis.ConnectionPool(port=6379,decode_responses=True)
	r = redis.Redis(connection_pool=pool)
	
	company_nodes_file(r,'companySpider:items','data/company_nodes.neo4j')
	person,management = person_and_management(r,'managementSpider:items')
	person_nodes_file(person,'data/person_nodes.neo4j')
	management_edges_file(management,'data/management_edges.neo4j')