
import redis
import scrapy
from scrapy.spiders import Spider
from get_url.items import GetUrlItem

r= redis.Redis(host='127.0.0.1',password='123321',port=6379,db=0)

class Spider(scrapy.Spider):
    name = 'get_url'

    start_urls =["https://list.jd.com/list.html?cat=9987,653,655",]
    for page in range(2,10):# 我们爬取前10页600个手机的详情url
        start_urls.append("https://list.jd.com/list.html?cat=9987,653,655"+"&page="+str(page))

    def parse(self,response):
        # 获得每一页的所有(60个)手机的详情url并添加到redis中
        item = GetUrlItem()
        for href in response.xpath('//li[@class="gl-item"]/div/div[4]/a/@href').extract():
            sku_url = response.urljoin(href)
            r.lpush('sku_urls',sku_url)
