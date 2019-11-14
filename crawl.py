# -*- coding: UTF-8 -*-
import requests,pymysql,time
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from models import first_crawl
from exts import db
import time
import re

flag = 0

#配置请求头
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection':'keep-alive',
    'Host':'www.cuc.edu.cn',
    'Upgrade-Insecure-Requests':'1',
    # 'Cookie':'BDTUJIAID=2ddf273cce81676ba59aece9bd9e47b2; Hm_lvt_f2fc44453e24fa1ffd7ca381e15e880d=1519136665,1519137091,1519188413; Hm_lpvt_f2fc44453e24fa1ffd7ca381e15e880d=1519188455',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox'
}
# 此处应手动配置你的数据库信息
def connect():
    conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='healthy', port=3306, charset='utf8')
    cur = conn.cursor()
    print("链接成功")


#def CrawlPage(page):
def CrawlPage(url, page, first_list_title):
    req = requests.session()
    req.headers = headers


    try:
        res = req.get(url, headers=headers,timeout=10)
    except RequestException as e:
        print("爬取"+str(page+1)+"页时响应未成功，休息5秒尝试再次请求~")
        return ["err", page]
    html = str(res.content, "utf-8")
    soup = BeautifulSoup(html, "html.parser")

    Link = soup.find_all("ul", attrs={"class": "news-list g-line"})
    for i in range(len(Link)):
        Linkq = str(Link[i])
        Dsoup = BeautifulSoup(Linkq, 'html.parser')
        title = Dsoup.find("a").get_text()
        if title not in first_list_title:
            titleurl = Dsoup.find("a").get('href')
            src = Dsoup.find('p').get_text()
            f_c = first_crawl(Title=title, NewsURL="http://www.cuc.edu.cn"+titleurl, src=src.split('|', 1)[0], time=src.split('|', 1)[1])
            db.session.add(f_c)
            db.session.commit()
            print("标题：", title)
            print("标题url：", "http://www.cuc.edu.cn"+titleurl)
            print(src.split('|', 1)[0])
            print("日期：", src.split('|', 1)[1])


def c_start_crawl1():
    page = 469

    # 提取数据库所有标题
    first_list = first_crawl.query.all()
    first_list_title = [];
    for fl in first_list:
        first_list_title.append(fl.Title)

    while(page > 0):
        print('\n', "爬取第" + str(page) + "页入口链接..")
        url = "http://www.cuc.edu.cn/news/1901/list" + str(
            page) + ".htm"
        UrlList = CrawlPage(url, page, first_list_title)
        print(UrlList)
        page -= 1


# if __name__ == "__main__":
#     Anum = 1
#     page = 1
#     while(page < 456):
#         print('\n',"爬取第"+str(page)+"页入口链接..")
#         url = "http://www.cuc.edu.cn/news/1901/list" + str(
#             page) + ".htm"
#         UrlList = CrawlPage(url)
#         page+=1


