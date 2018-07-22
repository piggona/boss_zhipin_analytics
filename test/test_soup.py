# author : haohao
# date : 18-7-19
# file_name : test_soup.py
from bs4 import BeautifulSoup
html = """
<div class="job-primary">
<div class="info-primary">
<h3 class="name">
<a data-index="1" data-itemid="1" data-jid="a5126e3b523034351Xd40921EFY~" data-jobid="23280804" data-lid="YqIC3NLWvE.search" href="/job_detail/a5126e3b523034351Xd40921EFY~.html" ka="search_list_1" target="_blank">
<div class="job-title">高级后台研发工程师</div>
<span class="red">20k-40k</span>
<div class="info-detail"></div>
</a>
</h3>
<p>北京  <em class="vline"></em>3-5年<em class="vline"></em>本科</p>
</div>
<div class="info-company">
<div class="company-text">
<h3 class="name"><a href="/gongsi/a67b361452e384e71XV82N4~.html" ka="search_list_company_1_custompage" target="_blank">今日头条</a></h3>
<p>移动互联网<em class="vline"></em>D轮及以上<em class="vline"></em>10000人以上</p>
</div>
</div>
<div class="info-publis">
<h3 class="name"><img src="https://img2.bosszhipin.com/boss/avatar/avatar_1.png"/>陈梅<em class="vline"></em>招聘者</h3>
<p>发布于07月17日</p>
</div>
</div>
"""

def for_soup(html):
    soup = BeautifulSoup(html)
    print(soup.prettify())


def main():
    for_soup(html)


if __name__ == "__main__":
    main()