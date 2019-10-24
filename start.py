from flask import Flask, redirect, url_for, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
import config
from models import first_crawl, second_crawl
from crawl import c_start_crawl1
from crawl2 import c_start_crawl2
import threading
import time
from multiprocessing import Process
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/jieba')
def jiebat():
    jieba.load_userdict("dict.txt")
    stopwords = [line.strip() for line in open("stopword.txt", 'r', encoding='utf-8').readlines()]

    allwords = []
    words_count = []
    result = ""
    news_titles =""
    search_content = "教育"

    news = first_crawl.query.filter(first_crawl.Title.like("%" + search_content + "%")).all()
    for each_news in news:
        each_title = each_news.Title
        news_titles = news_titles + " "+str(each_title)
        jieba_each_title = jieba.cut(each_title, cut_all=False)
        # jieba_each_title = jieba.cut_for_search(each_title)
        for word in jieba_each_title:
            if word not in allwords:
                if word not in stopwords:
                    if len(word) is not 1:
                        allwords.append(word)
                        words_count.append(1)
            else:
                words_count[allwords.index(word)] += 1



    print(allwords)
    print(words_count)
    print(len(allwords))
    print(len(words_count))
    print(news_titles)
    for word in allwords:
        result = result+" "+word

    n_t = jieba.cut(news_titles, cut_all=False)
    nt_r = " ".join(n_t)
    wc = WordCloud(
        font_path='simhei.ttf',  # 字体路劲
        background_color='white',  # 背景颜色
        width=1000,
        height=600,
        max_font_size=50,  # 字体大小
        min_font_size=10,
        # mask=None,
        mask=plt.imread('./static/images/3.png'),  # 背景图片
        max_words=1000
    )
    print(nt_r)
    wc.generate(nt_r)
    wc.to_file("./to_images/"+search_content+'.png')
        # print("Full Mode: " + "/ ".join(jieba_each_title))  # 全模式

    plt.figure('nt')  # 图片显示的名字
    plt.imshow(wc)
    plt.axis('off')  # 关闭坐标
    plt.show()


@app.route('/form', methods=['GET', 'POST'])
@app.route('/form/<int:page>', methods=['GET', 'POST'])
@app.route('/form/<string:search>/<int:page>/', methods=['GET', 'POST'])
def form(page=None, search=None):
    # if request.method == 'GET':
    #     cord = first_crawl.query.order_by(first_crawl.ID).paginate(page=page, per_page=50, error_out=False)
    #     return render_template('form.html', page_data=cord)
    # if request.method == 'POST':
    #     id = request.form.get("search_id")
    #     if id:
    #         if id.isdigit():
    #             u = first_crawl.query.filter(first_crawl.ID==id).order_by(first_crawl.ID).paginate(page=page, per_page=50, error_out=False)
    #             return render_template("form.html", page_data=u, search=id)
    #         else:
    #             count = first_crawl.query.filter(first_crawl.Title.like("%" + id + "%")).count()
    #             u = first_crawl.query.filter(first_crawl.Title.like("%" + id + "%")).order_by(first_crawl.ID).paginate(page=page,
    #                                                                                                  per_page=50,
    #                                                                                                  error_out=False)
    #             return render_template("form.html", page_data=u, search=id)
    #     else:
    #         u = first_crawl.query.order_by(first_crawl.ID).paginate(page=page, per_page=50, error_out=False)
    #         return render_template("form.html", page_data=u)
    search_content = request.form.get("search_id")
    if search_content:
        if search_content.isdigit():
            u = first_crawl.query.filter(first_crawl.ID == search_content).order_by(first_crawl.ID).paginate(page=page, per_page=50,
                                                                                                 error_out=False)
            return render_template("form.html", page_data=u, search=search_content)
        else:
            count = first_crawl.query.filter(first_crawl.Title.like("%" + search_content + "%")).count()
            u = first_crawl.query.filter(first_crawl.Title.like("%" + search_content + "%")).order_by(first_crawl.ID).paginate(
                page=page,
                per_page=50,
                error_out=False)
            return render_template("form.html", page_data=u, search=id)
    else:
        cord = first_crawl.query.order_by(first_crawl.ID).paginate(page=page, per_page=50, error_out=False)
        return render_template('form.html', page_data=cord)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/start_crawl1")
def start_crawl1():
    # t = threading.Thread(target=c_start_crawl1)
    # t.start()
    # t.join()
    c_start_crawl1()
    # p = Process(target=c_start_crawl1)
    # p.daemon = True
    # # # 启动进程
    # p.start()
    # ppid = p.pid
    # print(ppid)
    # p.join()

    return render_template("p.html")

import os, signal
def dd():
    print(ppid)
    os.kill(ppid, signal.signal())


@app.route("/start_crawl2")
def start_crawl2():
    c_start_crawl2()
    # print("***********************************************************************************")
    # p = Process(target=dd)
    # # # 启动进程
    # p.start()
    # p.join()
    # fg = 0
    # return render_template("p.html")
    pass


@app.route("/form2", methods=['GET', 'POST'])
@app.route('/form2/<int:page>', methods=['GET', 'POST'])
def form2(page=None):
    if request.method == 'GET':
        cord = second_crawl.query.order_by(second_crawl.ID).paginate(page=page, per_page=50, error_out=False)
        return render_template('form2.html', page_data=cord)
    else:
        id = request.form.get("search_id")
        if id:
            if id.isdigit():
                u = second_crawl.query.filter(second_crawl.ID==id).order_by(second_crawl.ID).paginate(page=page, per_page=10, error_out=False)
                return render_template("form2.html", page_data=u)
            else:
                u = second_crawl.query.filter(second_crawl.content.like("%" + id + "%")).order_by(second_crawl.ID).paginate(page=page,
                                                                                                     per_page=10,
                                                                                                     error_out=False)
                return render_template("form2.html", page_data=u)
        else:
            u = second_crawl.query.order_by(second_crawl.ID).paginate(page=page, per_page=10, error_out=False)
            return render_template("form2.html", page_data=u)

@app.route("/f_delete/", methods=['GET'])
def f_delete():
    Did = request.args.get('id')
    del_first_crawl = first_crawl.query.filter(first_crawl.ID == Did).first()
    print(del_first_crawl)
    from exts import db
    db.session.delete(del_first_crawl)
    db.session.commit()
    return redirect(url_for('form'))


@app.route("/s_delete/", methods=['GET'])
def s_delete():
    Did = request.args.get('id')
    del_second_crawl = first_crawl.query.filter(second_crawl.ID == Did).first()
    print(del_second_crawl)
    from exts import db
    db.session.delete(del_second_crawl)
    db.session.commit()
    return redirect(url_for('form2'))


if __name__ == '__main__':
    app.run(debug=True, threaded=True, processes=3)
