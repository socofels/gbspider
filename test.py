# 发送请求的库
import requests

import bs4

import time
import pandas as pd
import json

# 全局设置
# 网页地址
url1 = "http://www.csres.com/sort/"
url2 = "http://www.csres.com/sort/industry/002006_1.html"
# 头文件，这里从浏览器中可以找到
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
session = requests.session()
session.headers=headers
session.get(url1)
response = session.get(url2)
print(response)