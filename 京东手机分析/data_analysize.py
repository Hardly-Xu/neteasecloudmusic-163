# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class DataAnalysize(object):
    def __init__(self):
        with open('result.json') as f:
            data = pd.read_json(f)
            # 过滤掉CommentCount不足100的手机
            data = data[data.CommentCount > 100]
            # 通过价格大于400来过滤掉一些老年机
            data.price = data.price.str.replace('"', '')
            data.price = data.price.astype('float').astype('int')
            data = data[data.price > 400]
        self.data = data

    def plot_top_brand(self):
        top_brand = self.data.groupby('brand').size().sort_values(ascending=False)
        top_brand[:15].plot.pie(fontsize='small', title='品牌出镜率(前十五)')
        plt.show()

    def plot_brand_ratings(self):
        # 按品牌分组,然后计算其综合好评率
        brand_ratings = self.data.pivot_table('GoodRate', index='brand', aggfunc='mean').sort_values(by='GoodRate',ascending=False)
        brand_ratings.plot.bar(fontsize='small', title='品牌综合好评率', ylim=[0.9, 1], rot=45)
        plt.show()

    def plot_poor_rate(self):
        poor_rate = self.data.sort_values(by='PoorRate', ascending=False)
        # 筛选掉差评不足200的手机并取差评率最高的前20条数据  
        poor_rate = poor_rate[poor_rate.PoorCount > 200][:20]
        poor_rate.drop([774, 514, 977], inplace=True)  # 有几行name值为'',删掉
        # deal_name = lambda x:  还真不好处理,手动吧
        yticks = ['小米5C(3+64G)', '小米5C', '小米6(6+64G)', '华为荣耀8青春版(4+64)', '小米4A(2+16)', '红米4A(2+16)', '小米(4G+64G)',
                  'iPhone6(32G)', '飞利浦（PHILIPS）E350', '小米4A(2G+16G)', '小米6(4G+64G)', '三星GalaxyS8+', '小米Note2', '华为荣耀9',
                  'iPhone7(32)', 'iPhone7(32)', '三星GalaxyC5']
        poor_rate.index = yticks  # 更改下名字,不然图太丑了
        poor_rate.plot.barh()
        plt.show()

    def plot_average_price(self):
        average_price = self.data.groupby('brand').price.mean().sort_values()[-20:]
        ax = average_price.plot.bar(rot=30, title='各品牌手机的平均价格')
        ax.set(ylabel='平均价格')
        plt.show()


d = DataAnalysize()
d.plot_top_brand()
# d.plot_brand_ratings()
# d.plot_poor_rate()
# d.plot_average_price()
