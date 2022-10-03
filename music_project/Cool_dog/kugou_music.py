# 爬取视频页的网页源代码
from concurrent import futures
import json,sys
import requests
import time
from lxml import etree
import queue
import threading
# 请替换自己浏览器的cookie, 否则可能会被反爬

class KuGou(object):
    def __init__(self):
        self.url = 'https://www.kugou.com/yy/rank/home/1-49224.html?from=rank'
        self.headers = {
            'cookie': 'kg_mid=36c888254533a42aefa3231fae2b9a7b; kg_dfid=3exXXk2fqdZi1AL4KN10ezvW; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; ACK_SERVER_10015=%7B%22list%22%3A%5B%5B%22gzlogin-user.kugou.com%22%5D%5D%7D; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1656392490; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1656392605; KuGooRandom=66621656392605264',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }

    def get_data(self,url):
        list_html = requests.get(url, headers=self.headers).text
        return list_html

    def parse_data(self, data):
        html = etree.HTML(data)
        song_links = html.xpath('//a[@class="pc_temp_songname"]/@href')
        song_title = html.xpath('//a[@class="pc_temp_songname"]/@title')
        for i in range(len(song_links)):
            song_html = self.get_data(song_links[i])
            song_html = song_html.split('var dataFromSmarty = [')[1]
            song_html = song_html.split('],//当前页面歌曲信息')[0]
            # print(song_html)
            hash = json.loads(str(song_html))['hash']
            album_audio_id = json.loads(str(song_html))['mixsongid']
            down_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash=' + str(hash) + '&album_audio_id=' + str(album_audio_id)
            down_json = self.get_data(down_url)
            mp3_url = json.loads(str(down_json))['data']['play_url']
            mp3_lrc = json.loads(str(down_json))['data']['lyrics']
            # print(mp3_url)
            # print(mp3_lrc)
            mp3_content = requests.get(mp3_url, headers=self.headers).content
            self.save_data(song_title[i],mp3_content,mp3_lrc,i,)

    def save_data(self, song_title,mp3_content,mp3_lrc,i):
        with open(f'music/{song_title}.mp3', 'wb') as f:
            f.write(mp3_content)
        with open(f'music/{song_title}.lrc', 'w', encoding='utf-8') as f:
            f.write(mp3_lrc)
        print(i, song_title, 'mp3文件和歌词已经下载完毕')

    def run(self):
        url = self.url
        list_html = self.get_data(url)
        self.parse_data(list_html)

if __name__ == '__main__':
    kg = KuGou()
    start_time = time.time()
    kg.run()
    print('一共下载时间为',time.time()-start_time)


# print(list_html)

