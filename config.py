# author : haohao
# date : 18-7-21
# file_name : config.py
from get_pool import *

# headers = {
#     'Accept': "text/html,application/xhtml+xml,application/xml;",
#     'accept-encoding': "gzip",
#     'Accept-Language': "zh-CN,zh;q=0.8",
#     'Referer': "https://www.baidu.com/",
#     'cookie': "__c=1501326829; lastCity=101020100; __g=-; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.20.1.20.20; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502948718; __c=1501326829; lastCity=101020100; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502954829; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.21.1.21.21",
#     'pragma': "no - cache",
#     'upgrade - insecure - requests': '1',
#     'user-agent': "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19",
# }
headers = {
    'x-devtools-emulate-network-conditions-client-id': "5f2fc4da-c727-43c0-aad4-37fce8e3ff39",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'dnt': "1",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
    'cookie': "__c=1501326829; lastCity=101020100; __g=-; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.20.1.20.20; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502948718; __c=1501326829; lastCity=101020100; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502954829; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.21.1.21.21",
    'cache-control': "no-cache",
    'postman-token': "76554687-c4df-0c17-7cc0-5bf3845c9831"
}


# class proxy:
#     __proxy_dic = {}
#
#     def __init__(self):
#         self.__proxy_dic = get_proxy_val()
#
#     def get_proxy_dic(self):
#         return self.proxy_dic
#
#     def set_proxy_dic(self, proxies):
#         self.proxy_dic = proxies



def get_proxy_val():
    proxies = {
        "http": "http://" + get_proxy(),
        "https": "http://{}".format(get_proxy()),
    }
    return proxies


GROUP_START = 1
GROUP_END = 10

base = 'https://www.zhipin.com/job_detail/'

MONGO_URL = 'localhost'
MONGO_DB = 'bosszhipin'
MONGO_TABLE = 'bosszhipin'
