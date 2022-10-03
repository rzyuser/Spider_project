# -*- coding:utf-8 -*-
# @Environment: Python 3.7
import datetime
import requests
import sys
import time
import json

word_url = 'http://index.baidu.com/api/SearchApi/thumbnail?area=0&word={}'

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Host": "index.baidu.com",
        "Referer": "http://index.baidu.com/v2/index.html",
        # "Cipher-Text": "1652425237825_1652501356206_VBpwl9UG8Dvs2fAi91KToRTSAP7sDsQU5phHL97raPDFJdYz3fHf9hBAQrGGCs+qJoP7yb44Uvf91F7vqJLVL0tKnIWE+W3jXAI30xx340rhcwUDQZ162FPAe0a1jsCluJRmMLZtiIplubGMW/QoE/0Pw+2caH39Ok8IsudE4wGLBUdYg1/bKl4MGwLrJZ7H6wbhR0vT5X0OdCX4bMJE7vcwRCSGquRjam03pWDGZ51X15fOlO0qMZ2kqa3BmxwNlfEZ81l3L9nZdrc3/Tl4+mNpaLM7vA5WNEQhTBoDVZs6GBRcJc/FSjd6e4aFGAiCp1Y8MD66chTiykjIN51s7gbJ44JfVS0NjBnsvuF55bs="
        "Cipher-Text": "1654498873368_1654571274585_UDYRT6Pmup8lP3LaZAWiomM+1rMg3jmC1SvVMK3fXAD8nhd44wzlLXSQwbmBeFwyYWsPYWbHIBxjP5QYVFGFaaz17ntXV5bHlcr5Ytg1F2zUiHGBgaKJ2Crb2c7iu+qNXKQtysEcPimGDFr4p13Cz7of+0zfBG9jxEtriv5BfSTMVog6brCsHDdnUc5bJnRnJVHpFGnL9wsTLqbe0mLD3/Cr6bi6Mv1Ds9Js0Ps3YrwYllsx8YJwCIGxbcdOZIl8Qqv5GMQsZbEKL7+2h0KEdWvR5yGY0EbLlCa08m3NiVtK/79Nm+b+t93Tceu4eNBcr22v9Wi49npdrxyKsjk5kgK4RPzRC1K6fr1HFrBOb9Q=",
    }
    cookies = {
        'Cookie': 'BIDUPSID=CCC79887504B5B23F73EB6784310D843; PSTM=1651728138; BAIDUID=1C929E7DD7586A31EE867DC126A5DDEE:FG=1; ZFY=VPxgirSVeQ9A:AWKIg4LzaRLrb0S1g8Ig2ThXhya1M5U:C; BDRCVFR[-HoWM-pHJEc]=mk3SLVN4HKm; H_PS_PSSID=31253_26350; BA_HECTOR=0k218la4ag81ah8l8g1h9tea115; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1654569282; BDUSS=VXLXBoY0J6NHBxODdzR2xvSWdaRkJjb0JONUUyVlFjSjQ2cmF5azBkNXlSc1ppRVFBQUFBJCQAAAAAAAAAAAEAAAA0iiFCv8K~wsWj19AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHK5nmJyuZ5iTW; BDUSS_BFESS=VXLXBoY0J6NHBxODdzR2xvSWdaRkJjb0JONUUyVlFjSjQ2cmF5azBkNXlSc1ppRVFBQUFBJCQAAAAAAAAAAAEAAAA0iiFCv8K~wsWj19AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHK5nmJyuZ5iTW; CHKFORREG=dbd4f4c2eb9ea5629a2f7e51b1be98c9; Hm_up_d101ea4d2a5c67dab98251f0b5de24dc=%7B%22uid_%22%3A%7B%22value%22%3A%221109494324%22%2C%22scope%22%3A1%7D%7D; bdindexid=phv735hb4cgl0iglqpeta5k7b4; __yjs_st=2_YmU1MmNkN2NhMmI5YmY0NjhmZmYwMzkwNjE0NTFlOTE5MWYyZDIxZGIyYzUzYTk5ZWVhZmU2NjQ5NjRkNmE4ZmNjNTA3MTA4YTM5ZmU5MDBjM2IxMDQ5ZjcxNWNiOWU3MWFiYzZiZTU1Y2YyNjc5MmNiYWViZjg0MTFjMTU5ZWU2NTUwMWJmOTI2MTE0ZTE4NTQ3MDZmMjE5MmIzMjc2Y2UzOTdlY2RkNzg4MDliNjRiNDhiZjc1OWIzODc1ODUzXzdfZWUxOTE0NDE=; BAIDUID_BFESS=351DAB532D655604426A6A272EDBB23B:FG=1; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1654570328; ab_sr=1.0.1_MzJiOWRmNDliNGM5NmE1MTBlYTgzNzcwN2FmYWZlOWZkYzJmZTExMGJiODUxMjI3NTY4ZDU3NDMyZThmYWFmZjg2ZTNkMWZjZTEwMzgwZDM5YTI1MTMzN2YwOTVlM2E4NmFhNGNlNTE0NjFkNzI3NGViYTg1YTA1MWYyYWI0MTZjY2M5MDNhMTE4NTU3OWY5NmY4Mzg3YzE4OGI5ZTI1Yg==; RT="z=1&dm=baidu.com&si=nt4fw421tc&ss=l43jtxex&sl=l&tt=l3k&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=mfmh&ul=mm05"'
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    return response.text


def decrypt(t, e):
    n = list(t)
    i = list(e)
    a = {}
    result = []
    ln = int(len(n) / 2)
    start = n[ln:]
    end = n[:ln]
    for j, k in zip(start, end):
        a.update({k: j})
    for j in e:
        result.append(a.get(j))
    return ''.join(result)


def get_ptbk(uniqid):
    url = 'http://index.baidu.com/Interface/ptbk?uniqid={}'
    resp = get_html(url.format(uniqid))
    return json.loads(resp)['data']


def get_data(keyword, start='2011-01-02', end='2022-01-02'):
    url = "https://index.baidu.com/api/SearchApi/index?area=0&word=[[%7B%22name%22:%22{}%22,%22wordType%22:1%7D]]&startDate={}&endDate={}".format(keyword, start, end)
    print(url)
    data = get_html(url)
    print("data:  ",data)
    data = json.loads(data)
    print("data:  ",data)
    uniqid = data['data']['uniqid']
    print("uniqid:  ",uniqid)
    data = data['data']['userIndexes'][0]['all']['data']
    print("data:  ",data)
    ptbk = get_ptbk(uniqid)
    print("ptbk:  ",ptbk)
    result = decrypt(ptbk, data)
    print("result:  ",result)
    result = result.split(',')
    print("result:  ",result)
    start = start_date.split("-")
    print("start:  ",start)
    end = end_date.split("-")
    print("end:  ",end)
    a = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    print("a:  ",a)
    b = datetime.date(int(end[0]), int(end[1]), int(end[2]))
    print("b:  ",b)
    node = 0
    for i in range(a.toordinal(), b.toordinal()):
        date = datetime.date.fromordinal(i)
        print(date, result[node])
        node += 1


if __name__ == '__main__':
    keyword = "爬虫"
    start_date = "2022-01-02"
    end_date = "2022-05-02"
    get_data(keyword, start_date, end_date)
