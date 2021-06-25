import time

import bs4
import pandas as pd
from bs4 import BeautifulSoup
import requests


#查看请求信息
def showresponse(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    response = requests.get(url,headers=headers)
    print(bs4.BeautifulSoup(response.text))


# 爬取数据
def spide():
    response = requests.get('http://www.csres.com/sort/')

    return response.text


# 写入数据
def writefile(data, floderpath, filename):
    with open(floderpath + filename, 'a') as f:
        f.write(data)


def checkfloder(floderpath):
    None


testdata = []
if __name__ == '__main__':
    showresponse("http://www.csres.com/sort/industry.jsp")
# writefile(spide(),"F:\PL\ssl\gbspider","\\test")
