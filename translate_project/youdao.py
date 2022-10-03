import requests,time,random,hashlib,json

class YouDao(object):

    def __init__(self,kw):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-1634432869@10.169.0.82; OUTFOX_SEARCH_USER_ID_NCOO=1725553418.343504; JSESSIONID=aaaJ8MZSQyp5n-AGw3vux; ___rl__test__cookies=1602389687958',
            'Referer': 'http://fanyi.youdao.com/'
        }
        self.form_data = {}
        self.kw = kw

    def generate_form_data(self):
        # 通过python代码，模拟js的执行过程和结果
        # r = "" + (new Date).getTime()
        r = str(int(time.time() * 1000))
        # i = r + parseInt(10 * Math.random(), 10)
        rand_num = random.randint(0, 10)
        i = r + str(rand_num)
        # n.md5("fanyideskweb" + e + i + "]BjuETDhU)zqSxf-=B#7m")
        # md5加密："fanyideskweb" + 翻译内容 + salt + "]BjuETDhU)zqSxf-=B#7m"
        b = "fanyideskweb"
        m = "]BjuETDhU)zqSxf-=B#7m"
        temp_str = b + self.kw + i + m
        # hashlib.md5(temp_str).hexdigest()   与下面三行代码一样
        md5 = hashlib.md5()
        md5.update(temp_str.encode())
        sign = md5.hexdigest()
        self.form_data = {
            'i': self.kw,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': i,
            'sign': sign,
            'lts': r,
            'bv': '845c7a98930367a6f425519dfd188407',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME',
        }

    def get_data(self):
        resp = requests.post(self.url,headers=self.headers,data=self.form_data)
        return resp.content.decode()
        pass

    def parse_data(self,results):
        # 提取翻译结果
        dict_results = json.loads(results)
        data = dict_results['translateResult'][0][0]['tgt']
        print('翻译结果：',data)

    def run(self):
        self.generate_form_data()
        results = self.get_data()
        self.parse_data(results)

if __name__ == '__main__':
    youdao = YouDao('翻译')
    youdao.run()