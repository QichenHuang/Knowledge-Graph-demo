# 知识图谱的小demo
这是一个试图实现知识图谱的“微项目”，从头到尾的工作包括，从网上爬取格式化的数据，简单的数据处理，将数据存入图数据库中。  
关于知识图谱构建技术的相关知识详见附带的《知识图谱构建技术综述》  
嫌麻烦不想看论文可以简单看看[徐阿衡的博客 http://www.shuang0420.com/2017/09/05/项目实战-知识图谱初探/](http://www.shuang0420.com/2017/09/05/项目实战-知识图谱初探/) 补充一下理论知识

### 环境及工具
	Win10
	python 3.6.5
	scrapy
	scrapy_redis
	redis
	neo4j
### 目录及文件
当前目录为scrapy项目的根目录内，记为{SCRAPY_ROOT}  
{SCRAPY_ROOT}\  
| medicine_company_list.txt   公司编号代码文件  
| neo4j_import.bat   将处理后的data目录下的数据文件导入neo4j数据库中  
| neo4j_nodes_edges.py   将redis服务器中的数据处理后输出data目录下的三个文件  
| scrapy.cfg   srapy的配置文件  
| spiders_entry.py   开始爬取数据的入口
| urls.py   保存几个爬取网页的url  
| Crawlers   scrapy的项目目录  
| | ···  
| data   保存从redis导出后输出的数据文件  
| | company_nodes.neo4j 公司结点的数据  
| | person_nodes.neo4j 个人结点的数据  
| | management_edges.neo4j 公司和个人之间管理关系的数据  
| graph_demo.db   导入neo4j数据库后得到的数据库目录  
| | ···

### 项目运行流程
##### Step 1
运行`spiders_entry.py`文件,成功后数据保存在redis服务器中  
```
python spiders_entry.py [-h] [--host HOST] [--codefile CODEFILE] [--master MASTER] [--spiders SPIDERS]
optional arguments:  
  -h, --help           show this help message and exit  
  --host HOST          Redis服务器地址，默认为本地localhost  
  --codefile CODEFILE  公司代码列表，默认为 medicine_company_list.txt  
  --master MASTER      是master还是slave，1 表示master，0 表示slave，默认为 1  
  --spiders SPIDERS    选择爬虫，用逗号分隔，默认为 companySpider,managementSpider,noticeSpider  
```
##### Step 2
直接运行`neo4j_nodes_edges.py`文件，将redis服务器中的数据导出到data目录下的文件中
```
python neo4j_nodes_edges.py
```
##### Step 3
运行批处理文件`neo4j_import.bat`文件，将数据导入neo4j服务器中
```
.\neo4j_import
```
### 引用连接
这个项目主要思路参照[shuang0420的knowledge_graph_demo](https://github.com/Shuang0420/knowledge_graph_demo)  
附上一些可能用得上的教程：  
[python 廖雪峰教程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)  
[scrapy 官网教程](https://docs.scrapy.org/en/latest/intro/overview.html)  
[redis 菜鸟教程](http://www.runoob.com/redis/redis-tutorial.html)(这个项目用到的几乎只有`lpush/rpush`，不需要太深入)  
[scrapy_redis demo指南](https://github.com/rmax/scrapy-redis)  
[neo4j w3cschool教程](https://www.w3cschool.cn/neo4j/)(很详细，但是很罗嗦)  
### 其他事项
1. 这个项目主要参照`shuang0420的knowledge_graph_demo`的思路走，在数据方面的一些问题，如文件`medicine_company_list.txt`的来源未知，准确率和覆盖率没有细究，所以在导入neo4j数据库的时候提示出现了一堆`referring to missing node`的错误，不过对其他导入的结点不影响，就没有纠结这个地方。
2. 爬虫爬取的数据包括公司信息，个人信息及管理关系，还有公司的公告信息，这里存入neo4j只考虑了公司和个人的管理关系，因为对公告的处理涉及到自然语言技术，所以暂时没有考虑，造成的结果就是每个公司（包括其管理人员）都是孤立的结点。
3. 使用neo4j_import.bat将数据导入neo4j数据库时有可能出现乱码现象，需要将data目录下的三个文件转换为`utf-8无BOM编码`
