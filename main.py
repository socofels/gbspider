# -*- coding: utf-8 -*-
# 发送请求的库
import requests
import bs4
from tqdm import tqdm
import time
import json

# 全局设置
# 网页地址
url = "http://www.csres.com/sort/industry.jsp"
# 头文件，这里从浏览器中可以找到
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

# 网页的基础url，这个项目后面要用到
baseurl = "http://www.csres.com/"

session = requests.session()
session.get(url)
session.headers = headers


# 获取网站信息
def spide(url, headers):
    # 简历一个会话，保持链接，解决cookie访问的问题

    # 设置头文件，模拟浏览器登录，可以在浏览器中查找得到
    response = requests.get(url, headers=headers)

    # 查看返回的文件
    # print(bs4.BeautifulSoup(response.text))

    # 设置编码，防止因为文字编码导致错误
    response.encoding = response.apparent_encoding

    # 获取页面内容
    content = response.text

    return content, session.cookies


# 解析网站的信息
def getdata(content):
    # 使用bs4解析，解析器使用的是html.parser，还可以选择lxml，解析作用是从网页内容中提取有用信息
    data = bs4.BeautifulSoup(content, "html.parser")
    # # 这里示例获取第一个匹配到的超链接
    # print('获取第一个匹配到的超链接', data.a)
    # # 2 属性
    # # data.标签名.attrs # 获取标签中所有属性名与对应属性值的字典
    # print('获取超链接中所有属性名与对应属性值的字典', data.a.attrs)  # 获取超链接中所有属性名与对应属性值的字典
    # # data.标签名.attrs["属性名"]获取属性名对应的属性值
    # print('获取超链接href属性对应的属性值', data.a.attrs["href"])  # 获取超链接href属性对应的属性值
    # # data.标签名["属性名"]获取属性名对应的属性值的简写
    # print('获取超链接href属性对应的属性值的简写', data.a["href"])  # 获取超链接href属性对应的属性值的简写
    # # data.标签名.string  # 获取第一个匹配到的标签的内容
    # print('获取第一个匹配到的超链接的内容', data.a.string)  # 获取第一个匹配到的超链接的内容
    # # data.标签名.text  # 获取第一个匹配到的标签以及其所包含的子标签的所有内容
    # print('获取第一个匹配到的超链接以及其所包含的子标签的所有内容', data.a.text)  # 获取第一个匹配到的超链接以及其所包含的子标签的所有内容
    #
    # # 3 函数
    # # data.标签名.get_text()  # 同data.标签名.text
    # print(data.a.get_text())  # 同data.a.text
    #
    # # data.find("标签名") # 同data.标签名
    # print(data.find("a"))  # 同data.a
    # print(data.find("a", href="/detail?dbname=life&num=35"))  # 根据属性值定位到第一个匹配到的标签

    # # 注意： 若属性名是 class 则需要在后面加个下划线,写成 class_
    # # data.find_all("标签名") # 获取匹配到的所有标签, 返回一个列表
    # a_list = data.find_all("a")  # 获取所有的超链接
    # for a in a_list:  # 循环查看每个超链接的文字和url
    #     if a.string is None:  # 如果超链接的内容为空
    #         continue
    #     else:
    #         print(a.string + ":" + a.get("href"))
    # # data.find_all(["标签1", "标签2"])   可以获取多种类的标签，通过列表指定获取的多个标签
    # data.find_all(["a", "div"])  # 可以获取多种类的标签，通过列表指定获取的多个标签
    # # data.find_all("标签名", limit=int(n))  # limit参数指定获取个数，为整数
    # # print(data.find_all("a", limit=2))  # 获取前2个匹配到的超链接

    # 通过查找获取到所有国标的链接
    categorylists = data.find_all("a", class_="sh14lian")
    lists = []
    for item in categorylists:
        if item.text is None:
            continue
        else:
            # 整理证字典，名字和链接
            link = item.get("href")
            link = link[1:]
            lists.append([item.text.split("[")[0], link])

    # print(lists)
    return lists


# todo 现在能爬取一页的数据了，接下来考虑分类爬取并保存
def spide2(lists):
    mylist = []
    for item in tqdm(lists):
        print("正在下载", item[0])
        # todo 需要在这里循环下一页，对每一页进行爬取
        link = baseurl + item[1]
        data = session.get(link)
        soup = bs4.BeautifulSoup(data.text, "html.parser")
        thead = soup.find("thead")
        # print(thead)
        try:
            tr = thead.find_all("tr", bgcolor="#FFFFFF")
            for item in tr:
                i = item.find_all("td")
                arr = []
                for j in i:
                    arr.append(j.text)
                mylist.append([arr[0].split("\xa0")[1], arr[1].split("\xa0")[1], arr[4]])
        finally:
            None
        # data=json.dumps(mylist)
        print(mylist)


# 写入数据
def writefile(data, floderpath, filename):
    with open(floderpath + filename, 'a') as f:
        f.write(data)


def checkfloder(floderpath):
    testdata = []


if __name__ == '__main__':
    # 获取第一级内容
    content, cookies = spide(url, headers)

    # 解析第一级内容，返回得到二级网页的数组
    lists = getdata(content)

    # 打开二级网页,爬取需要的数据
    content2 = spide2(lists)

# writefile(spide(),"F:\PL\ssl\gbspider","\\test")
