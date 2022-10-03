# 爬取视频页的网页源代码 --> 提取数据包 --> 提取 play_url -- > base64解码 --> 获取视频 --> 获取音频 --> 合并视频和音频

# 爬取视频页的网页源代码
import os
import pprint
import re
import json
import requests
import base64
# 请替换自己浏览器的cookie, 否则可能会被反爬
headers = {
    'cookie': 'MONITOR_WEB_ID=b1af876f-96a9-4f7c-9e81-bc0fae58b4e4; support_webp=true; support_avif=true; ixigua-a-s=1; ttcid=9c9460622d634e189fda6abcc2cc101122; _tea_utm_cache_1300=undefined; tt_scid=MuRD1bUAEgxvzohIGAXePUWbVJ5JOAHnISlaWBY0JYqfdN4mi82iyQ1lZnnY3EOf40ba; ttwid=1%7CJS9xlpuQGgsVKw4VwQF0mUAzyxMHz5M46jxwPCUejcM%7C1655556382%7Cd183462d1a90ebf9bac8f5563c2165a238d8b162f5fd5007ecb31ec8fd3e1591; msToken=xzqlC21GcjrrqvKPNNSH5Hh8hTjO3opsoD4BZqGSMsggx9b0DoRkPitC4Nky0N8nrRNpdEPz5eyKTE-dt5g3j66dyfQ7H2qvljBYkYUhV8B6nM-VJmo9; __ac_nonce=062adddf300fec10b2c7f; __ac_signature=_02B4Z6wo00f01RG9ngQAAIDAcrdeb9o-VZURnZqAACbFVh2ZcxEdUY6Zvt-zMknJjYMgivmKBlN3l-4eBp4G3cCVR7TOD.QkNciS8i5AG34Jiwt0sD42z7Fu0Dc8KPUL3VBPnvDBQRZoaStl51; __ac_referer=https://www.ixigua.com/6805142209797554702?id=6762751596301386247&logTag=6e80e7a62475886a63ab',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}
url = 'https://www.ixigua.com/6805142209797554702?id=6762751596301386247&logTag=6e80e7a62475886a63ab'

r = requests.get(url,headers=headers)
r.encoding = r.apparent_encoding
# print(r.text)

# 提取数据包
temp = re.findall('_SSR_HYDRATED_DATA=(.*?)</script>',r.text)[0].replace('undefined','null')
video_url = json.loads(temp)["anyVideo"]["gidInformation"]['packerData']['video']["videoResource"]['dash']["dynamic_video"]['dynamic_video_list'][-1]['main_url']
audio_url = json.loads(temp)["anyVideo"]["gidInformation"]['packerData']['video']["videoResource"]['dash']["dynamic_video"]['dynamic_audio_list'][-1]['main_url']
filename = json.loads(temp)["anyVideo"]["gidInformation"]['packerData']['video']["title"]

# pprint.pp(audio_url)
print('开始下载..音频和视频')
video_url_decode = base64.b64decode(video_url).decode()
audio_url_decode = base64.b64decode(audio_url).decode()
video_content = requests.get(video_url_decode,headers=headers).content
audio_content = requests.get(audio_url_decode,headers=headers).content
with open(f'video/{filename}.mp4','wb') as f:
    f.write(video_content)
print(f'已完成视频{filename}部分下载')
with open(f'video/{filename}.mp3','wb') as f:
    f.write(audio_content)
print(f'已完成音频{filename}部分下载')

# ffmpeg
cmd = fr"D:\test\ffmpeg-5.0.1-full_build\bin\ffmpeg -i video\{filename}.mp4 -i video\{filename}.mp3 -c:v copy -c:a aac -strict experimental video\output{filename}.mp4  -loglevel quiet"

os.system(cmd)
print('已完成合并...')
os.remove(f'video/{filename}.mp3')
print('已删除冗余的音频')
os.remove(f'video/{filename}.mp4')
print('已删除冗余的视频')


