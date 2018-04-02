# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy, re, json
from scrapy_redis.spiders import RedisSpider
from get_detail.items import get_detail
from scrapy import Request


class Spider(RedisSpider):
    name = 'master' #复制到docker容器中时记得改名如:slave_1
    redis_key = 'sku_urls'

    def parse(self, response):
        item = get_detail()
        info = response.xpath('//div[@class="p-parameter"]')
        raw_name = response.xpath('//div[@class="sku-name"]/text()').extract()
        item['name']  = ''.join(str(raw_name[-1]).split())
        item['product_id']= response.url.split('/')[-1].split('.')[0]
        item['more_info'] = info.xpath('//ul[contains(@class, "parameter2")]/li/text()').extract()
        try:
            item['resolution']= info.xpath('//li[@class="fore0"]/div/p/text()').extract()
            item['camera']= info.xpath('//li[@class="fore1"]/div/p/text()').extract()
            cpu_info = info.xpath('//li[@class="fore2"]/div/p/text()').extract()
            item['cpu']= {'核数':cpu_info[0][9:],'频率':cpu_info[1][9:]}
        except:
            item['cpu']= '暂无信息'
            item['camera']= '暂无信息'
            item['resolution']= '暂无信息'

        try:
            item['brand']= response.xpath('//*[@id="parameter-brand"]/li/a/text()').extract()
        except:
            item['brand']= '暂无信息'
        # 因为直接爬信息详情页是获取不到京东价格的, 所以换了个url来查询其价格, 其中爬取到的价格如果为'-1',代表该商品已经下架
        price_url = 'http://p.3.cn/prices/mgets?skuIds=J_'+re.sub(r'\D', '',response.url)
        request = Request(url=price_url, callback=self.parse_price)
        request.meta['item'] = item
        return request

    def parse_price(self,response):
        item = response.meta['item']
        if not str(response.body)[1:-5].split(':')[-1]=='-1':
            item['price'] = str(response.body)[1:-5].split(':')[-1]
        else:
            item['price'] = '已下架'
        product_id = item['product_id']
        comments_url = 'http://club.jd.com/ProductPageService.aspx?method=GetCommentSummaryBySkuId&referenceId='+product_id
        request = Request(url=comments_url, callback=self.parse_comments)
        request.meta['item'] = item
        return request

    def parse_comments(self,response):
        item = response.meta['item']
        comments_dict=json.loads(response.body_as_unicode())
        item['CommentCount']=comments_dict.get('CommentCount')
        item['GoodCount']=comments_dict.get('GoodCount')
        item['DefaultGoodCount']=comments_dict.get('DefaultGoodCount')
        item['GoodRate']=comments_dict.get('GoodRate')
        item['PoorCount']=comments_dict.get('PoorCount')
        item['PoorRate']=comments_dict.get('PoorRate')
        item['AfterCount']=comments_dict.get('AfterCount')

        return item 