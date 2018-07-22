# author : haohao
# date : 18-7-21
# file_name : spider.py
"""
多线程，多代理定时爬虫
爬取boss直聘招聘信息，并规整化数据为json格式
存储于Mongodb中
"""

import pymongo
import time

from config import *
from utils.get_summary import *
from utils.make_html import *
from urllib.parse import urlencode
from get_pool import *
import requests
import ssl
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def save_to_mongo(result):
    """
    去重&存储
    :param result: 得到的json数据
    :return: 存储状态
    """
    if db[MONGO_TABLE].find({"detail_url": result["detail_url"]}) is None:
        if db[MONGO_TABLE].insert(result):
            print('存储成功', result)
            return True
        return False


def get_page_index(offset):
    """
    得到首页重要信息
    :param offset: 网站分页的页面
    :return: 首页信息
    """
    data = {
        'page': offset
    }
    params = urlencode(data)
    url = base + '?' + params
    print(url)
    try:
        response = requests.get(url, headers=headers, allow_redirects=False,
                                proxies=p)
        # print(response.text)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 302:
            pass
            # need Proxy
        else:
            print("请求错误" + str(response.status_code))
            return None
    except ConnectionError:
        print('Error occured')
        get_page_index(offset)
        return None


def parse_page_index(html):
    """
    1. 得到简略信息
    2. 得到详细信息的url
    3. 获取详细信息
    :param html: 页面信息(html)
    :return: 规整的json
    """
    # print(html)
    soup = BeautifulSoup(html, "lxml")
    contexts = soup.select('.job-list ul li .job-primary')
    # print(contexts)
    # pattern = re.compile('<div class="info-primary">.*?<h3 class="name">.*?<a href="(.*?)".*?class ="job-title" >(.*?)</div>.*?<span class="red">(.*?)<span>',re.S)
    for context in contexts:
        context = make_html(context)
        # print(context)
        primary_info = get_primary_info(context)
        primary_info = make_html(primary_info)
        title = get_title(primary_info)
        place = get_place(primary_info)
        experience = get_experience(primary_info)
        salary = get_salary(primary_info)
        # 获取基本信息
        page_url = get_url(primary_info)
        detail_index = parse_detail_index(page_url)
        # 获取详细文本
        company_name = get_company_info(context)
        # 获取公司名称
        date = get_date(context)
        # 获取发布时间
        summary_info = {
            "title": title,
            "place": place,
            "experience": experience,
            "salary": salary,
            "detail_url": page_url,
            "detail_index": detail_index,
            "company_name": company_name,
            "date": date
        }
        print(summary_info)
        save_to_mongo(summary_info)


def get_detail_index(detail_url):
    """
    获取详细信息页面
    :param detail_url: 详细信息url
    :return: 详细信息页面
    """
    url = "https://www.zhipin.com" + detail_url
    print(url)
    try:
        response = requests.get(url, headers=headers, proxies=p)
        print(response.status_code)
        if response.status_code == 200:
            return response.text
        else:
            print("访问失败")
    except ConnectionError:
        print("ERROR OCCURED")
        get_detail_index(detail_url)


def parse_detail_index(detail_url):
    """
    获取详细信息url
    :param detail_url: 详细信息未加工url
    :return: 详细信息url
    """
    html = get_detail_index(detail_url)
    soup = BeautifulSoup(html, 'lxml')
    contexts = soup.select('.detail-content .job-sec .text')
    result = contexts[0].get_text().strip('<br/>')
    result = result.strip()
    print(result)
    return result


def main(offset):
    ssl._create_default_https_context = ssl._create_unverified_context
    html = get_page_index(offset)
    print("获取网页成功")
    # print(html)
    parse_page_index(html)


if __name__ == '__main__':
    while True:
        p = get_proxy_val()
        pool = Pool()
        groups = ([x for x in range(GROUP_START, GROUP_END + 1)])
        try:
            pool.map(main, groups)
            pool.close()
            # main(1)
            time.sleep(1800)
        except Exception:
            print("proxy不可用")
