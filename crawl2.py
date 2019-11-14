# -*- coding: UTF-8 -*-
import requests, re, sys
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import urllib.request
from models import first_crawl, second_crawl
from exts import db
import os


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

def CrawlPage(url, flag):
    req = requests.session()
    req.headers = headers
    second_list = second_crawl.query.all()
    second_title_list = []
    for sl in second_list:
        second_title_list.append(sl.Title)
    try:
        res = req.get(url, headers=headers,timeout=10)
    except RequestException as e:
        print("爬取"+"页时响应未成功，休息5秒尝试再次请求~")
        return ["err"]
    html = str(res.content, "utf-8")
    soup = BeautifulSoup(html, "html.parser")

    if flag is 1:
        # Link = soup.find_all("span",attrs={"class":"WP_VisitCount"})

        title = soup.find('h1').get_text()
        if title not in second_title_list:
            article = soup.find("article", attrs={"class", "con-area"}).get_text()
            newsurl = url
            visit_time = soup.find("span", attrs={'class', 'WP_VisitCount'}).get_text()
            src = soup.find("span", attrs={'class', 'arti-name'}).get_text().replace(' ', '').split('0', 1)[0][5:].split("\r", 1)[0]
            time = soup.find("span", attrs={'class', 'arti-name'}).get_text().replace(' ', '').split('0', 1)[1][:8]
            print(article)
            print(newsurl)
            print(visit_time)
            print(title)
            print(src)
            print(time)
            s_c = second_crawl(Title=title, content=article, NewsURL=newsurl, visit_time=visit_time, src=src, time=time, )
            db.session.add(s_c)
            db.session.commit()

    if flag is 2:
        folder_path = 'E:\Photo\\'+title
        if os.path.exists(folder_path) == False:
            os.makedirs(folder_path)

        reg_jpg = "/_upload.*?.jpg|/_upload.*?.png"
        img_src = str(soup.find_all("article", attrs={"class", "con-area"})).split("<")
        imglist = []
        for i_s in img_src:
            imgre = re.compile(reg_jpg)
            imglist_jpg = imgre.findall(str(soup.find_all("article", attrs={"class", "con-area"})))
            if len(imgre.findall(i_s)) is not 0:
                imglist.append(imgre.findall(i_s)[0])
        x = 0
        for img in imglist:
            img = "http://www.cuc.edu.cn"+img
            print(img)
            urllib.request.urlretrieve(img, 'E:\Photo\\'+title+"\\"+'%s.jpg' % x)  # 下载图片
            break
            x += 1


def c_start_crawl2():
    cord = first_crawl.query.filter()
    for u in cord:
        print(u.NewsURL, u.ID)
        url = u.NewsURL
        if url.endswith('/page.htm'):
            # if u.ID > 16:
            CrawlPage(url, 1)

# if __name__=="__main__":
#     # url ="http://www.cuc.edu.cn/news/2019/1008/c1901a140383/page.htm"
#     # url="http://www.cuc.edu.cn/news/2019/0926/c1901a139514/page.htm"
#     cord = first_crawl.query.filter()
#     for u in cord:
#         print(u.NewsURL, u.ID)
#         url = u.NewsURL
#         if url.endswith('/page.htm'):
#             if u.ID >16:
#                 CrawlPage(url)


def c_start_crawl2_images():
    cord = first_crawl.query.filter()
    for u in cord:
        print(u.NewsURL, u.ID)
        url = u.NewsURL
        if url.endswith('/page.htm'):
            # if u.ID > 16:
            CrawlPage(url, 2)