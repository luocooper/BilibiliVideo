# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:49:21 2022

@author: 86152
"""

import requests
from lxml import html
import re
import json
import os
#from moviepy.editor import *
#import ffmpeg
# =============================================================================
# >>>ffmpeg 常用命令总结<<<
# -i xxx.mp3 传入文件
# xxx.wav 输出.wav 格式的文件 直接写在最后，不用在前面加啥
# -f wav 强制规定输出的格式为wav
# -y 覆盖输出文件 不是覆盖输入文件，ffmpeg不能覆盖输入，只能用os.remove('xxx.mp3')
# acodec 就是audio codec  音频编译器 可以写 copy 也可以写具体编码
# ab 就是audio bits 音频码率可以写128k 代表128kpbs/s
# =============================================================================



def get_title_json(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
    }
    r = requests.get(url, headers=head)
    tree = html.fromstring(r.text)
    title = str(tree.xpath('//*[@id="viewbox_report"]/h1/@title')[0])
    s = ['\n', '，', '。', ' ', '—', '”', '？', '“', '（', '）', '、','|']
    for i in s:
        title = title.replace(i, '') 
    print(f'视频标题："{title}"')

    json_data = re.findall('<script>window.__playinfo__=(.*?)</script>', r.text)[0]
    json_data = json.loads(json_data)
    audio_url = json_data['data']['dash']['audio'][0]['backupUrl'][0]
    print('已提取到音频地址')
    video_url = json_data['data']['dash']['video'][0]['backupUrl'][0]
    print('已提取到视频地址')
    return title,audio_url,video_url


def download(title,audio_url,video_url):
    head = {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67',
                  'Referer':url
    }
    print('开始下载音频')
    r_audio = requests.get(url=audio_url, headers=head)
    audio_data = r_audio.content
    with open(title+'.mp3', mode='wb') as f:
        f.write(audio_data)
    print('音频下载完成')

    print('开始下载视频')
    print('下载中,请稍等...') #慢的是请求这一步
    r_video = requests.get(url=video_url, headers=head)
    video_data = r_video.content
    with open(title+'.mp4', mode='wb') as f:
        f.write(video_data)
    print('视频下载完成')

def audio_video_add(title):
    print('开始合成')
# =============================================================================
#     #摆脱了ffmpeg,但是合成很慢
#     video = VideoFileClip(title+'.mp4')
#     audio = AudioFileClip(title+'.mp3')
#     video1 = video.set_audio(audio)
#     video1.write_videofile(f'bili_{title}.mp4')
# =============================================================================
    #ffmpeg-python这个库还不成熟，而且也不知到要不要下载ffmpeg
    #ffmpeg.concat(ffmpeg.input(title+'.mp4'),ffmpeg.input(title+'.mp3')).output('out.mp4')
    cmd=f' ffmpeg  -i {title}.mp4 -i {title}.mp3 -acodec copy -vcodec copy bili_{title}.mp4'
    os.system(cmd) 
    #cmd使用前，要保证ffmpeg是环境变量，如果提示不是可执行的，请重启电脑!!!
    os.remove(title+'.mp4')
    os.remove(title+'.mp3')
    print('合成结束')
    
if __name__ == "__main__":   
    while True:
        value = input('输入该视频的有效链接地址：(输入quit退出）')
        if value=='quit':
            break
        else:
            url=value
            
            title,audio_url,video_url=get_title_json(url)
            
            download(title,audio_url,video_url)
            
            audio_video_add(title)
            
    #应该再加一个异常处理
    
