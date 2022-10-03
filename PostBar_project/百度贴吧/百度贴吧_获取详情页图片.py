import os
import requests
from lxml import etree
import pandas as pd

class BaiDuTieBa(object):
    def __init__(self,word):
        self.word = word
        self.url = "https://tieba.baidu.com/f?ie=utf-8&kw=" + self.word
        self.headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 101.0.4951.64Safari / 537.36Edg / 101.0.1210.47',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': 'BIDUPSID=8E824BCF6338F003C48D122624CF7C2F; PSTM=1640785171; BAIDUID=8E824BCF6338F0032A6DF35FB9C359B6:FG=1; __yjs_duid=1_36c4edfb136ea4abe3fe3b0928d9d4be1641369130708; H_WISE_SIDS=107316_110085_127969_131862_174441_179345_184716_188744_189037_189755_190627_190792_191068_191243_191287_191370_192206_192391_192958_193284_194085_194511_194520_195342_195631_196425_196514_197242_197286_197470_197711_197782_197958_198122_198254_199082_199177_199469_199489_199569_199753_199995_200349_200434_200763_201055_201104_201358_201444_201548_201553_201577_201706_201733_201979_201996_202115_202298_202392_202563_202760_202894_202915_202927_203072_203248_203265_203314_203504_203606_203630_203749_203987_204098_204112_204205_204375_204430_8000083_8000101_8000128_8000137_8000150_8000162_8000169_8000177_8000185_8000189; BDUSS=Ek3YW03V29tWTQ2YWtBaE5VUlVXVWxTeldJWHZVUmF5US1Hd245cX56T25uM2hpRVFBQUFBJCQAAAAAAAAAAAEAAAA0iiFCv8K~wsWj19AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKcSUWKnElFid; BDUSS_BFESS=Ek3YW03V29tWTQ2YWtBaE5VUlVXVWxTeldJWHZVUmF5US1Hd245cX56T25uM2hpRVFBQUFBJCQAAAAAAAAAAAEAAAA0iiFCv8K~wsWj19AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKcSUWKnElFid; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BAIDUID_BFESS=8E824BCF6338F0032A6DF35FB9C359B6:FG=1; BDRCVFR[7FEYkXni5q3]=mk3SLVN4HKm; BA_HECTOR=842g0k8l840ka5812k1h8dskv14; ZFY=NefznUyC8K9b:BOUnTJG2dxDy92wMFWXpDhquswxY4mw:C; delPer=0; PSINO=5; BDRCVFR[OEHfjv-pq1f]=I67x6TjHwwYf0; H_PS_PSSID=; STOKEN=9f03963ed77e11a034bc22cc9e839049dcb19dc4a9112987d20f99a8d189b205; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1651577963,1653028120; 1109494324_FRSVideoUploadTip=1; video_bubble1109494324=1; BAIDU_WISE_UID=wapp_1653028142513_549; USER_JUMP=-1; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1653028199'
        }
    def get_data(self,url):
        resp = requests.get(url,headers=self.headers)
        return resp.content
    def parse_data(self,data):
        data = data.decode().replace("<!--", "").replace("-->", "")
        html = etree.HTML(data)
        el_list = html.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a')
        data_list = []
        for el in el_list:
            temp = {}
            temp['title'] = el.xpath('./text()')[0]
            temp['url'] = 'https://tieba.baidu.com' + el.xpath("./@href")[0]
            print(temp)
            data_list.append(temp)
        try:
            next_url = 'https:' + html.xpath('//a[contains(text(),"下一页>")]/@href')[0]
        except:
            next_url = None
        return data_list,next_url

    def parse_detail(self,data):
        html = etree.HTML(data.decode())
        image_list = html.xpath('//*[@class="BDE_Image"]/@src')
        return image_list
    def save_data(self, data):
        data_list1 = []
        for i in data:
            data_list1.append(list(i.values()))
        data_pd = pd.DataFrame(data_list1,columns=['title','link'])
        if not os.path.exists('csv'):
            os.mkdir('csv')
        else:
            if not os.path.exists('./csv/result.csv'):
                data_pd.to_csv("./csv/result.csv",index=False,mode='a',encoding='utf-8-sig')
            else:
                data_pd.to_csv("./csv/result.csv",index=False,mode='a',encoding='utf-8-sig',header=False)

    def download(self,image_list):
        if not os.path.exists('images'):
            os.mkdir('images')
        else:
            if not os.path.exists('./images/' + self.word):
                os.mkdir('./images/' + self.word)
            else:
                for image_url in image_list:
                    image_bytes = self.get_data(image_url)
                    image_name = image_url.split('/')[-1].split('?')[0]
                    print(image_name)
                    with open('./images' + os.sep + self.word + os.sep + image_name, 'wb') as f:
                        f.write(image_bytes)

    def run(self):
        next_url = self.url
        while True:
            data = self.get_data(next_url)
            data_list,next_url = self.parse_data(data)
            print(next_url)
            self.save_data(data_list)
            for tieba in data_list:
                detail_data = self.get_data(tieba['url'])
                image_list = self.parse_detail(detail_data)
                self.download(image_list)
            if next_url == None:
                break
if __name__ == '__main__':
    # bdtb = BaiDuTieBa('王者荣耀')
    bdtb = BaiDuTieBa('迪丽热巴')
    bdtb.run()