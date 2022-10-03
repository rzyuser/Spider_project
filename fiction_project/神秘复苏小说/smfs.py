import re
import os
import requests,time
from lxml import etree
from multiprocessing.dummy import Pool
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

start_url = 'https://www.dddbiquge.cc/book/45082839.html'
headers = {

            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }

def get_source(url):
    html = requests.get(url,headers=headers, verify=False)
    # print(html.text)
    return html.text  # 这个网页需要使用gbk方式解码才能让中文正常显示

"""
获取每一章链接，储存到一个列表中并返回
:param html: 目录页源代码
:return: 每章链接
"""
def get_article_url(html):
    article_url_list = []
    data = etree.HTML(html)
    data_list = data.xpath('//dd/a/@href')
    for url in data_list[12:]:
        article_url_list.append('https://www.dddbiquge.cc' + url)
    return article_url_list

"""
获取每一章的正文并返回章节名和正文
:param html: 正文源代码
:return: 章节名，正文
"""
def get_article(html):
    chapter_name = re.findall('<h1>(.*?)</h1>', html, re.S)[0]
    # print(chapter_name)
    text_block = re.findall('</script>(.*?)<script>app2', html, re.S)[-1]
    text_block = text_block.replace('&nbsp;', '')           # 替换 &nbsp; 网页空格符
    text_block = text_block.replace('<br />', '\n')
    return chapter_name, text_block

"""
将每一章保存到本地
:param chapter: 章节名, 第X章
:param article: 正文内容
:return: None
"""
def save(chapter, article):
    os.makedirs('神秘复苏', exist_ok=True)  # 如果没有"北欧众神"文件夹，就创建一个，如果有，则什么都不做"
    with open(os.path.join('神秘复苏', chapter + '.txt'), 'w', encoding='utf-8') as f:
        f.write(article)
    print(chapter,'保存成功')

"""
根据正文网址获取正文源代码，并调用get_article函数获得正文内容最后保存到本地
:param url: 正文网址
:return: None
"""
def query_article(url):
    article_html = get_source(url)
    chapter_name, article_text = get_article(article_html)
    # print(chapter_name)
    # print(article_text)
    save(chapter_name, article_text)

if __name__ == '__main__':
    start_time = time.time()
    toc_html = get_source(start_url)
    toc_list = get_article_url(toc_html)
    # for i in toc_list:
    pool = Pool(5)
    pool.map(query_article, toc_list)
    #     query_article(i)
    print('一共下载时间为',time.time()- start_time)




