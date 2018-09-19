'''
    更新于2018年9月,仅供学习入门参考,无任何反爬措施.
    paramas:
        歌单id(PLAYLIST_ID),目标用户(TARGET_ID),根据自己需求更改.
'''
import time
import json
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from my_crypt import crypt_api


PLAYLIST_ID = {'id': 907742221}
TARGET_ID = 44814771
HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Cookie':'_ntes_nnid=73794490c88b2790756a23cb36d25ec1,1507099821594; _ntes_nuid=73794490c88b2790756a23cb36d25ec1; _ngd_tid=LtmNY2JGJkw6wR3HF%2FpG2bY%2BtHhQDmOj; usertrack=c+xxC1nazueHBQJiCi7XAg==; JSESSIONID-WYYY=sJg6dw45PFKjn0VD2OuD0mzqC03xb3CnU3h4ac43kp7r9q9GJos%2BFDVyZmeGtz%5CHciN66cY5KAEW6jlHT%5COv0qzP8T3O3R5cq28%2BXJ3rc%2BkqsI4Y%2BrJIwZczDZGlvq225U%5CNWBP0iEjTnfdUG21swAhZA%5CfX29F4s9M6tz2EK7%2FESIpW%3A1507612773856; _iuqxldmzr_=32; MUSIC_U=e58d5af1daeedff199dcb9d14e06692f2db7395809fd3b393c0d6d53e13de2f484b4ab9877ef4e4ca1595168b12a45da86e425b9057634fc; __remember_me=true; __csrf=63e549f853ed105c4590d6fe622fb4f6',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/',
    'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
}

def get_json(url, data, only_total=False):
    """get given music_id's comment info"""
    response = requests.post(url=url, headers=HEADER, data=data)
    if only_total:
        return json.loads(response.content.decode("utf-8"))['total']
    return json.loads(response.content.decode("utf-8"))['comments']


def get_comment(play_list):
    cm_cnt = 0
    offset = 0
    res = defaultdict(list)
    while True:
        try:
            music_id, music_name = play_list.pop()
        except KeyError:
            break

        url, data = crypt_api(music_id, 0)
        # 获取评论总数, 以便带入不同offset获得每一页的评论
        cnt = get_json(url, data, only_total=True)
        # 获取一首歌的所有评论(每页20条):
        for offset in range(0, cnt, 20):
            url, data = crypt_api(music_id, offset)
            json_comment = get_json(url, data)
            for comment in json_comment:
                user_id = comment['user']['userId']
                if user_id == TARGET_ID:
                    user_name = comment['user']['nickname']
                    cm = comment['content']
                    page = -((cnt // 20 + 1) - offset // 20)
                    res[user_name].append({'评论内容': cm, '歌曲名':music_name, '歌曲id':music_id, '所在页数(倒数)': page, })
            print('每爬取一页(20条)评论sleep 1 秒...')
            time.sleep(1)
        cm_cnt += cnt
    print('爬取完成!总爬取{}条评论.'.format(cm_cnt))
    if res:
        print('正在写入结果...')
        fn = '{}.txt'.format(time.strftime('%m-%d %H:%M', time.localtime()))
        with open(fn, 'w') as fp:
            json.dump(res, fp, indent=2, ensure_ascii=False)
        print('写入完成')


def get_playlist_info(play_list_id):
    """获取playlist中的所有music的name/id
        return: {(music_id, music_name}
    """
    res = set()
    r = requests.get('http://music.163.com/playlist', params=play_list_id)
    body = BeautifulSoup(r.content.decode(), 'html.parser').body
    info = body.find('ul', attrs={'class': 'f-hide'}).find_all('li')
    for i in info:
        music_id = i.find('a')['href'].replace('/song?id=', '')
        music_name = i.find('a').getText()
        res.add((music_id, music_name))
    return res


if __name__ == '__main__':
    play_list = get_playlist_info(PLAYLIST_ID)
    get_comment(play_list)
