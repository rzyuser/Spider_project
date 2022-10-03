"""
只能手机上复制链接在在从中提取链接爬取视频
"""

import httpx

# url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAcud_llwUN1kpfpzeb3Xqbq8nsRwU7lxVzg3OSv31hNMPz95UspEw1L53dX-UDrE4&count=2155375401000"
url = 'https://m.douyin.com/web/api/v2/aweme/post/?reflow_source=reflow_page&sec_uid=MS4wLjABAAAACelAT-rXmCSiIppfxalDbNoqvvmVxvLY46LARowbDYk&count=21&max_cursor=0'  # 请求头
headers = {
    # "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "accept-language": "zh-CN,zh;q=0.9"
}

# 访问json数据连接
resp = httpx.get(url, headers=headers)
print(resp.json())
# resp = json.loads(resp.content)
# print(resp)
# 拿到JSON数据,并解析
data = resp.json()["aweme_list"]
# data = resp["aweme_list"]

for i in data:
    # 视频地址
    video = i["video"]["play_addr"]["url_list"][0]
    print(video)
    # 视频名称
    video_name = i["desc"]
    # 获取视频内容
    video_content = httpx.get(video, headers=headers).content
    # 下载视频
    # with open("./video/{}.mp4".format(video_name),"wb") as file:
    with open("./{}.mp4".format(video_name), "wb") as file:
        print("=" * 10, video_name, "正在下载中", "=" * 10)
        file.write(video_content)
