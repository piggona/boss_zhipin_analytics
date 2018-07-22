# author : haohao
# date : 18-7-21
# file_name : get_pool.py
import requests
from bs4 import BeautifulSoup
import lxml


def get_proxy():
    try:
        response = requests.get('http://127.0.0.1:5010/get')
        print(response.text)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


# if __name__ == "__main__":
#     get_proxy()
