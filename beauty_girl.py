# coding:utf-8
import requests
import os
import time
from threading import Thread
from collections import deque
from bs4 import BeautifulSoup

session = requests.Session()
img_url_list = deque()

def get_girl_list():
    response = session.get("http://www.win4000.com/zt/xinggan.html")
    content = response.content
    soup = BeautifulSoup(content, "html5lib")
    div = soup.find("div", {"class": "tab_box"})
    tag = div.find("ul", {"class": "clearfix"})
    li_list = tag.find_all("li")
    for li in li_list:
        link_tag = li.find("a")
        url = link_tag.attrs['href']  # 一个系列图片的链接
        name = link_tag.find("p").text  # 一个系列图片的名字

        get_girl_detail(name, url)
    else:
        get_girl_detail(None, None)

# 解析图片详细
def get_girl_detail(name, url):
    # 如果没有 url 了就传一个 None
    if url == None:
        img_url_list.append([None, None])
        return

    response = session.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html5lib")
    tag = soup.find("div", {"class": "scroll-img-cont"})
    li_list = tag.find_all('li')
    for li in li_list:
        img_url = li.find('img').attrs['data-original']
        img_url = img_url[0:img_url.find('_')] + '.jpg'
        img_url_list.append([name, img_url])

# 保存大图
def save_image():
    name_bak = ""
    count = 0
    while True:
        # 从 img_url_list 获取链接，直到获取到 None 退出
        try:
            name, img_url = img_url_list.popleft()
        except IndexError:
            continue

        if img_url == None:
            break

        print img_url
        img_response = requests.get(img_url)
        if not os.path.exists("images"):
            os.mkdir("images")
        # 根据名字来排列
        if name != name_bak:
            name_bak = name
            count = 0
        else:
            count += 1

        with open("images/%s_%d.jpg" %(name, count), 'wb') as f:
            f.write(img_response.content)

if __name__ == '__main__':
    get_list_thread = Thread(target=get_girl_list)
    get_img_thread = Thread(target=save_image)

    get_list_thread.start()
    get_img_thread.start()

    get_list_thread.join()
    get_img_thread.join()
