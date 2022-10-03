from lxml import etree
import requests,os,time
from multiprocessing.dummy import Pool
# url = 'https://bing.ioliu.cn/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
}

# with open('1.html','w',encoding='utf-8') as f:
#     f.write(test.decode())

wallpaper_urlss = []
def list_url():
    if not os.path.exists('./images'):
        os.mkdir('./images')
    j = 1
    while j<=50:
        url = 'https://bing.ioliu.cn/?p=' + str(j)
        test = requests.get(url, headers=headers).content
        html = etree.HTML(test.decode())
        wallpaper_url = html.xpath('//div[@class="card progressive"]/a/@href')
        wallpaper_urls = ['https://bing.ioliu.cn' + i for i in wallpaper_url]
        print(wallpaper_urls)
        for i in range(len(wallpaper_urls)):
            test1 = wallpaper_urls[i]
            image_byte = requests.get(test1, headers=headers)
            html = etree.HTML(image_byte.content.decode())
            url1 = html.xpath('/html/body/div/div[3]/a[3]/@href')
            print(url1[0])
            try:
                wallpaper_urlss.append(url1[0])
            except Exception:
                continue
        print(f'第{j}页链接获取完毕{wallpaper_urlss}')
        j+=1
        time.sleep(3)
    return wallpaper_urlss
r = 1
def details(url):
        global r
        image_bytes = requests.get(url, headers=headers)
        with open('./images' + os.sep + str(r) + '.jpg', 'wb') as f:
            f.write(image_bytes.content)
            r += 1
if __name__ == '__main__':
    start_time = time.time()
    lists = list_url()
    print('一共获取详情页时间为', time.time() - start_time)
    pool = Pool(5)
    pool.map(details, lists)
    print('一共下载时间为', time.time() - start_time)
