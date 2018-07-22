# author : haohao
# date : 18-7-21
# file_name : make_html.py
from bs4 import BeautifulSoup


def make_html(context):
    context = str(context)
    context = BeautifulSoup(context, 'lxml')
    context = context.prettify()
    return context
