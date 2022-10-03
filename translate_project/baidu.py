import requests,json
import execjs
"""
http://ifanyi.iciba.com/index.php?c=trans&m=fy&client=6&auth_user=key_ciba&sign=fcc710ee8531159d
"""

class BaiDufy(object):
    def __init__(self,language_contant):
        self.url = 'https://fanyi.baidu.com/v2transapi?'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32",
            'Cookie': 'BIDUPSID=CCC79887504B5B23F73EB6784310D843; PSTM=1651728138; BAIDUID=1C929E7DD7586A31EE867DC126A5DDEE:FG=1; ZFY=DlrE0AMPveYfy:BGM:B1ltj3qJvJvjbBs276GhLGIQsFs:C; BAIDU_WISE_UID=wapp_1653386342707_115; BA_HECTOR=042k8l048l8l2000ag1h8pd5k15; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1653389651; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1653389651; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; ab_sr=1.0.1_NDYyOTRlOWUzYWZhYjM5MWRmODVmYzgzMDI1ZjZiODQ0Y2RjNWY3YmM0NmY5ODkxNmQyZmE4MDNlMjY2N2VmNmQ5MmZlZDAwOWFmOGMyNTYxYWE1ODg0MzQ4NGU5NzJlYTMxMzkyNzZjNzUxMzkxMDdjMDhiZDFiZDMwZmYxZTkzMDI5ZjZkM2I1YTk2YWExNWExNDIzYmI4Mjg4M2RjMw=='
        }
        with open("a.js", 'r') as f:
            resp = f.read()
        self.sign = execjs.compile(resp).call('e', language_contant)
        self.data = {
            'from': 'auto',
            'to': 'auto',
            'query': language_contant,
            'sign': self.sign,
            'token': '6ffa75aabb04ffc9f178646d39d55a69',
        }
    def post_data(self):
        resp = requests.post(self.url,headers=self.headers,data=self.data)
        return resp.content.decode()
    def parse_data(self,datas):
        data_dict = json.loads(datas)
        print(data_dict)
        print(data_dict['trans_result']['data'][0]['dst'])
    def run(self):
        result = self.post_data()
        self.parse_data(result)
if __name__ == '__main__':
    word = input("请输入你要翻译的中文或英文")
    b = BaiDufy(word)
    b.run()