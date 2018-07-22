# author : haohao
# date : 18-7-18
# file_name : get_summary.py
import datetime
import re
from bs4 import BeautifulSoup


def get_primary_info(html):
    soup = BeautifulSoup(html, 'lxml')
    context_pri = soup.select('.info-primary')
    return context_pri[0]


def get_company_info(html):  # 得到公司名称
    soup = BeautifulSoup(html, 'lxml')
    context_co = soup.select('.info-company .company-text .name a')
    for result in context_co:
        return result.get_text().strip()


def get_place(html):  # 公司地点
    soup = BeautifulSoup(html, 'lxml')
    context_co = soup.select('p')
    pattern = re.compile("<p>(.*?)<em", re.S)
    for context in context_co:
        # print(context)
        result = re.findall(pattern, str(context))
        result = str(result).strip("[]\\n")
        # print(result)
        result = result[6:-7]
        return result.strip()


def get_experience(html):
    soup = BeautifulSoup(html, 'lxml')
    context_co = soup.select('p')
    pattern = re.compile("/em>(.*?)<em", re.S)
    for context in context_co:
        # print(context)
        result = re.findall(pattern, str(context))
        result = str(result).strip("[]\\n")
        result = result[6:-7]
        # print(result)
        return get_level(result.strip())


def get_date(html):
    soup = BeautifulSoup(html, 'lxml')
    context = soup.select('.info-publis p')
    for context_date in context:
        context_date = context_date.get_text()
        # print(context_date)
        # pattern = re.compile(".*?发布于(.*?)", re.S)
        # result = re.findall(pattern, context_date)
        # print(result)
        return parse_date(context_date.strip())


def get_url(html):
    soup = BeautifulSoup(html, 'lxml')
    url = soup.select('a')
    for result in url:
        return result['href']


def get_title(html):
    soup = BeautifulSoup(html, 'lxml')
    text = soup.select('a .job-title')[0].get_text()
    return text.strip()


def get_salary(html):
    soup = BeautifulSoup(html, 'lxml')
    text = soup.select(".red")[0].get_text()
    return parse_salary(text.strip())


# 提取(parse)函数
def parse_salary(text):
    salary_list = text.replace("k", "000").split("-")
    salary_list = [int(x) for x in salary_list]
    salary = {
        'low': salary_list[0],
        'high': salary_list[1],
        'avg': (salary_list[0] + salary_list[1]) / 2
    }
    return salary


def parse_date(context):
    result = context.replace("发布于", "2018-")
    result = result.replace("月", "-")
    result = result.replace("日", "")
    if result.find("昨天") > 0:
        result = str(datetime.date.today() - datetime.timedelta(days=1))
    elif result.find(":") > 0:
        result = str(datetime.date.today())
    return result


def get_level(text):
    level = 10
    if '应届生' in text:
        level = 1
    elif '1年以内' in text:
        level = 2
    elif '1-3年' in text:
        level = 3
    elif '3-5年' in text:
        level = 4
    elif '5-10年' in text:
        level = 5
    elif '10年以上' in text:
        level = 6
    elif '经验不限' in text:
        level = 0
    else:
        print("未知")
    return level


html = ("\n"
        "<html>\n"
        " <body>\n"
        "  <div class=\"job-primary\">\n"
        "   <div class=\"info-primary\">\n"
        "    <h3 class=\"name\">\n"
        "     <a data-index=\"1\" data-itemid=\"1\" data-jid=\"9350e2ee7f6b52961Xd-3t28F1E~\" data-jobid=\"23450173\" data-lid=\"YEZ1ZPpQtx.search\" href=\"/job_detail/9350e2ee7f6b52961Xd-3t28F1E~.html\" ka=\"search_list_1\" target=\"_blank\">\n"
        "      <div class=\"job-title\">\n"
        "       高级PHP开发工程师\n"
        "      </div>\n"
        "      <span class=\"red\">\n"
        "       25k-30k\n"
        "      </span>\n"
        "      <div class=\"info-detail\">\n"
        "      </div>\n"
        "     </a>\n"
        "    </h3>\n"
        "    <p>\n"
        "     上海\n"
        "     <em class=\"vline\">\n"
        "     </em>\n"
        "     5-10年\n"
        "     <em class=\"vline\">\n"
        "     </em>\n"
        "     本科\n"
        "    </p>\n"
        "   </div>\n"
        "   <div class=\"info-company\">\n"
        "    <div class=\"company-text\">\n"
        "     <h3 class=\"name\">\n"
        "      <a href=\"/gongsi/33c752360fee04a91HN_3t26.html\" ka=\"search_list_company_1_custompage\" target=\"_blank\">\n"
        "       伊碧思\n"
        "      </a>\n"
        "     </h3>\n"
        "     <p>\n"
        "      社交网络\n"
        "      <em class=\"vline\">\n"
        "      </em>\n"
        "      未融资\n"
        "      <em class=\"vline\">\n"
        "      </em>\n"
        "      100-499人\n"
        "     </p>\n"
        "    </div>\n"
        "   </div>\n"
        "   <div class=\"info-publis\">\n"
        "    <h3 class=\"name\">\n"
        "     <img src=\"https://img.bosszhipin.com/beijin/mcs/useravatar/20160926/84a53f0f723524389b609e148515d0f970c0a6f2fa9dc9a5290fc909c6872659_s.jpg\"/>\n"
        "     Bill huang\n"
        "     <em class=\"vline\">\n"
        "     </em>\n"
        "     招聘经理\n"
        "    </h3>\n"
        "    <p>\n"
        "     发布于昨天\n"
        "    </p>\n"
        "   </div>\n"
        "  </div>\n"
        " </body>\n"
        "</html>\n")


# def main():
#     company_test = get_date(html)
#     print(company_test)
#
#
# if __name__ == "__main__":
#     main()
