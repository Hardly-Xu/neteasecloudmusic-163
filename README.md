# NeteaseCloudMusic/网易云音乐
### Get comments of given playlist and find all the comments of the given user.
### 获取某用户(user_id)某歌单()下的所有评论

**2018年9月更新**: (若需最初我入门Python时的版本,请`ckeck out`至 `17d976a`)
仅供学习入门参考, 为了不给服务器照成不良影响(而不是像版本1那样一秒几百条的爬取, 获取评论的时候每请求一次(获取一页评论) sleep 1 秒,所以,粗略估算效率不到20条(可能17 ,18吧)评论/秒.

<br>

<hr>

**原README.md(2017年10月)**`git check out 17d976a`(慎用, 可能被反爬)

这是以前爬取结果的示例图片:

![实例图1](https://github.com/xuhaer/neteasecloudmusic-163/blob/master/1.jpeg)

![实例图2](https://github.com/xuhaer/neteasecloudmusic-163/blob/master/2.jpeg)

这是一个简陋的获取网易云音乐给定歌单的所有评论或找出特定用户在其歌单中的评论的程序。

说明：共有两个.py程序，大体上相同，只有一处不同点————多线程处理的思路上:

  * PLAN A：爬取网易云音乐给定歌单或用户的评论(歌曲多线程).py

       思路是先获取给定歌单中的所有歌曲的music_id，然后把music_id进行多线程处理，相当于一次爬取多首音乐的评论，然后再join.


* PLAN B:爬取网易云音乐给定歌单或用户的评论(评论多线程).py

       思路是先获取给定歌单中的所有歌曲的music_id，然后一次处理一个music_id，其后对该music_id下的评论进行多线程处理，相当把该歌曲的评论分为2部分，同时爬取，然后再join

注：PLAN A爬取速度取决于连续3首歌曲中评论数的最大值，实际上要比PLAN B慢。用我电脑爬取时速度大概在1M评论/h.


