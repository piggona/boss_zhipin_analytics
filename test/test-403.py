# author : haohao
# date : 18-7-19
# file_name : test-403.py
from urllib.parse import urlencode
from config import *

import requests
import urllib
import random

data = {
    'page': 1
}
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
           "Accept-Encoding": "gzip",
           "Accept-Language": "zh-CN,zh;q=0.8",
           "Referer": "http://www.baidu.com/",#需要加入上一位置信息
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
           }

params = urlencode(data)
url = base + '?' + params


def get_content(url, headers):
    '''
    @获取403禁止访问的网页
    '''
    try:
        response = requests.get(url, headers=headers)
        print(response.text)
        if response.status_code == 200:
            return response.text
        else:
            print("请求错误" + str(response.status_code))
            return None
    except ConnectionError:
        print('Error occured')
        return None


def main():
    get_content(url, headers)


if __name__ == '__main__':
    main()
