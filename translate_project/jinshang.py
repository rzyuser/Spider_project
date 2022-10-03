#coding:utf-8
import json

import requests

class King(object):

    def __init__(self,word):
        self.url = f"https://dict.iciba.com/dictionary/word/suggestion?ck=709a0db45332167b0e2ce1868b84773e&client=6&is_need_mean=1&nums=5&timestamp=1651491399670&uid=0&word={word}&signature=d4fa7058d0fc34c1c0bd0358d49dec0a&_=1651491408356"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"
        }
    def post_data(self):
        #使用post方法发送一个post请求，data为请求体的字典
        #response = requests.post(self.url,data=self.data,headers=self.headers)
        response = requests.get(self.url,headers=self.headers)
        return response.content

    def parse_data(self, data):
        #loads方法讲json数据转换成python字典
        dict_data = json.loads(data)
        # print(dict_data)
        # print(dict_data['content']['out'])
        print(dict_data['message'][0]['paraphrase'])

    def run(self):
        # url
        # headers
        # post——data
        # 发送请求
        data = self.post_data()
        # 解析
        self.parse_data(data)

if __name__ == '__main__':
    word = input("请输入要翻译的单词或句子")
    k = King(word)
    k.run()