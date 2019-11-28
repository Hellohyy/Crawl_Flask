from flask import Flask, redirect, url_for, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
import config
from models import first_crawl, second_crawl
from crawl import c_start_crawl1
from crawl2 import c_start_crawl2, c_start_crawl2_images
from pyecharts.charts import WordCloud
import threading
import time
from multiprocessing import Process
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index2')
def base2():
    return render_template("Generation_Two/index.html")


@app.route('/D3Force')
def D3Force():
    return render_template("Generation_Two/D3Force.html")


@app.route('/toActivecloud')
def toActivecloud():
    return render_template("Generation_Two/toActivecloud.html")


@app.route('/ActiveCloud', methods=['GET', 'POST'])
def ActiveCloud():
    keyword = request.form.get("search_word")
    jieba.load_userdict("dict.txt")
    stopwords = [line.strip() for line in open("stopword.txt", 'r', encoding='utf-8').readlines()]

    allwords = []
    words_count = []
    news_titles = ""
    search_content = keyword

    news = first_crawl.query.filter(first_crawl.Title.like("%" + search_content + "%")).all()
    for each_news in news:
        each_title = each_news.Title
        news_titles = news_titles + " " + str(each_title)
        jieba_each_title = jieba.cut(each_title, cut_all=False)
        for word in jieba_each_title:
            if word not in allwords:
                if word not in stopwords:
                    if len(word) is not 1:
                        allwords.append(str(word))
                        words_count.append(1)
            else:
                words_count[allwords.index(word)] += 1
    word_list = []
    dict_sort = {}
    dict = {}

    fileObject = open("./static/test.json", 'w')
    for i in range(len(allwords)):
        dict[allwords[i]] = words_count[i]

    print(len(dict))
    # fileObject.write(json.dumps(dict, ensure_ascii=False))
    # fileObject.close()
    return render_template("Generation_Two/ActiveCloud.html", datas=json.dumps(dict, ensure_ascii=False))


@app.route('/WordCloudData', methods=['GET', 'POST'])
def WordCloudData():
    if request.method == 'POST':
    # if kd is not None:
        keyword = request.form.get("search_word")

        # return render_template("D3Chart.html", words_list=word_list, allwords=allwords, words_count=words_count)
        # return render_template("Generation_Two/D3Chart.html", words_list=word_list, words=sorted(dict_sort.items(), key=lambda d:d[1], reverse=True), keyword=keyword)
    else:
        #return render_template("Generation_Two/D3Chart.html", words_list=None, words=None, keyword="输入关键词")
        keyword = "教育"
    jieba.load_userdict("dict.txt")
    stopwords = [line.strip() for line in open("stopword.txt", 'r', encoding='utf-8').readlines()]

    allwords = []
    words_count = []
    news_titles = ""
    search_content = keyword

    news = second_crawl.query.filter(second_crawl.content.like("%" + search_content + "%")).all()
    # news = first_crawl.query.filter(first_crawl.Title.like("%" + search_content + "%")).all()
    for each_news in news:
        each_title = each_news.Title
        news_titles = news_titles + " " + str(each_title)
        jieba_each_title = jieba.cut(each_title, cut_all=False)
        for word in jieba_each_title:
            if word not in allwords:
                if word not in stopwords:
                    if len(word) is not 1:
                        allwords.append(str(word))
                        words_count.append(1)
            else:
                words_count[allwords.index(word)] += 1
    word_list = []
    dict_sort = {}
    for i in range(len(allwords)):
        dict_sort[allwords[i]] = words_count[i]
        dict = {}
        dict['text'] = allwords[i]
        dict['size'] = words_count[i]
        word_list.append(dict)
    return render_template("Generation_Two/D3Chart.html", words_list=word_list,
                           words=sorted(dict_sort.items(), key=lambda d: d[1], reverse=True), keyword=keyword)


@app.route('/click_WordCloudData/<string:kd>', methods=['GET', 'POST'])
def click_WordCloudData(kd):
    keyword = kd
    jieba.load_userdict("dict.txt")
    stopwords = [line.strip() for line in open("stopword.txt", 'r', encoding='utf-8').readlines()]

    allwords = []
    words_count = []
    news_titles = ""
    search_content = keyword

    news = first_crawl.query.filter(first_crawl.Title.like("%" + search_content + "%")).all()
    for each_news in news:
        each_title = each_news.Title
        news_titles = news_titles + " " + str(each_title)
        jieba_each_title = jieba.cut(each_title, cut_all=False)
        for word in jieba_each_title:
            if word not in allwords:
                if word not in stopwords:
                    if len(word) is not 1:
                        allwords.append(str(word))
                        words_count.append(1)
            else:
                words_count[allwords.index(word)] += 1
    word_list = []
    dict_sort = {}
    for i in range(len(allwords)):
        dict_sort[allwords[i]] = words_count[i]
        dict = {}
        dict['text'] = allwords[i]
        dict['size'] = words_count[i]
        word_list.append(dict)
    print(len(word_list))
    return render_template("Generation_Two/D3Chart.html", words_list=word_list,
                           words=sorted(dict_sort.items(), key=lambda d: d[1], reverse=True), keyword=keyword)


# Python 词云图
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
        news_titles = news_titles + " "+ str(each_title)
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
    search_content = request.form.get("search_id")
    if search_content:
        if search_content.isdigit():
            u = first_crawl.query.filter(first_crawl.ID == search_content).order_by(first_crawl.ID).paginate(page=page, per_page=50,
                                                                                                 error_out=False)
            return render_template("Generation_Two/form.html", page_data=u, search=search_content)
        else:
            count = first_crawl.query.filter(first_crawl.Title.like("%" + search_content + "%")).count()
            u = first_crawl.query.filter(first_crawl.Title.like("%" + search_content + "%")).order_by(first_crawl.ID).paginate(
                page=page,
                per_page=50,
                error_out=False)
            return render_template("Generation_Two/form.html", page_data=u, search=id)
    else:
        cord = first_crawl.query.order_by(first_crawl.ID).paginate(page=page, per_page=50, error_out=False)
        return render_template('Generation_Two/form.html', page_data=cord)


@app.route('/form_sortBydate/', methods=['GET', 'POST'])
@app.route('/form_sortBydate/<int:page>', methods=['GET', 'POST'])
def form_sortBydate(page=None):
    count = first_crawl.query.filter().count()
    u = first_crawl.query.filter().order_by(first_crawl.time).paginate(
        page=page,
        per_page=50,
        error_out=False)
    return render_template("Generation_Two/form.html", page_data=u, search=id)


@app.route('/form2_sortBydate/', methods=['GET', 'POST'])
@app.route('/form2_sortBydate/<int:page>', methods=['GET', 'POST'])
def form2_sortBydate(page=None):
    count = second_crawl.query.filter().count()
    u = second_crawl.query.filter().order_by(second_crawl.time.desc()).paginate(
        page=page,
        per_page=50,
        error_out=False)
    return render_template("Generation_Two/form2.html", page_data=u, search=id, count=count)


@app.route('/form2_sortByvisit_time/', methods=['GET', 'POST'])
@app.route('/form2_sortByvisit_time/<int:page>', methods=['GET', 'POST'])
def form2_sortByvisit_time(page=None):
    count = second_crawl.query.filter().count()
    u = second_crawl.query.filter().order_by(second_crawl.visit_time.desc()).paginate(
        page=page,
        per_page=50,
        error_out=False)
    return render_template("Generation_Two/form2.html", page_data=u, search=id, count=count)


@app.route("/index")
def index():
    return render_template("Generation_Two/index.html")


@app.route("/start_crawl1")
def start_crawl1():
    # t = threading.Thread(target=c_start_crawl1)
    # t = threading.Thread(target=a)
    # t.start()
    # t.join()
    c_start_crawl1()
    # # p = Process(target=c_start_crawl1)
    # # p.daemon = True
    # # # # 启动进程
    # # p.start()
    # # ppid = p.pid
    # # print(ppid)
    # # p.join()

    return render_template("Generation_Two/p.html")


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


@app.route("/start_crawl")
def start_crawl():
    c_start_crawl1()
    c_start_crawl2()


@app.route('/search_form/', methods=['GET', 'POST'])
@app.route('/search_form/<int:page>', methods=['GET', 'POST'])
# @app.route('/search_form/<string:search>/<int:page>', methods=['GET', 'POST'])
def search_form(page=None, search=None):
    if page is None:
        page = 1
    search_content = request.form.get("search_id")
    if search_content.isdigit():
        u = first_crawl.query.filter(first_crawl.ID == search_content).order_by(first_crawl.ID).paginate(page=page, per_page=50,
                                                                                             error_out=False)
        return render_template("Generation_Two/search_form.html", page_data=u, search=search_content)
    else:
        count = first_crawl.query.filter(first_crawl.Title.like("%" + search_content + "%")).count()
        u = first_crawl.query.filter(first_crawl.Title.like("%" + search_content + "%")).order_by(first_crawl.ID).paginate(
           page=page,
            per_page=count,
            error_out=False)
        return render_template("Generation_Two/search_form.html", page_data=u, search=id)


@app.route('/start_crawl2_images', methods=['GET', 'POST'])
def start_crawl2_images():
    c_start_crawl2_images()


@app.route("/form2", methods=['GET', 'POST'])
@app.route('/form2/<int:page>', methods=['GET', 'POST'])
def form2(page=None):
    if request.method == 'GET':
        count = second_crawl.query.filter().count()
        cord = second_crawl.query.order_by(second_crawl.ID).paginate(page=page, per_page=50, error_out=False)
        return render_template('Generation_Two/form2.html', page_data=cord, count=count)
    else:
        id = request.form.get("search_id")
        if id:
            if id.isdigit():
                u = second_crawl.query.filter(second_crawl.ID==id).order_by(second_crawl.ID).paginate(page=page, per_page=10, error_out=False)
                return render_template("Generation_Two/form2.html", page_data=u, count=1)
            else:
                count = second_crawl.query.filter(second_crawl.content.like("%" + id + "%")).count()
                u = second_crawl.query.filter(second_crawl.content.like("%" + id + "%")).order_by(second_crawl.ID).paginate(page=page,
                                                                                                     per_page=10,
                                                                                                     error_out=False)
                return render_template("Generation_Two/form2.html", page_data=u, count=count)
        else:
            count = second_crawl.query.filter().count()
            u = second_crawl.query.order_by(second_crawl.ID).paginate(page=page, per_page=10, error_out=False)
            return render_template("Generation_Two/form2.html", page_data=u, count=count)


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


@app.route("/wordcloud", methods=['GET', 'POST'])
def wordcloud():
    # if request.method == 'GET':
    name = [
        'Sam S Club', 'Macys', 'Amy Schumer', 'Jurassic World', 'Charter Communications',
        'Chick Fil A', 'Planet Fitness', 'Pitch Perfect', 'Express', 'Home', 'Johnny Depp',
        'Lena Dunham', 'Lewis Hamilton', 'KXAN', 'Mary Ellen Mark', 'Farrah Abraham',
        'Rita Ora', 'Serena Williams', 'NCAA baseball tournament', 'Point Break']
    value = [
        10000, 6181, 4386, 4055, 2467, 2244, 1898, 1484, 1112,
        965, 847, 582, 555, 550, 462, 366, 360, 282, 273, 265]
    return render_template("Generation_Two/pie.html")


@app.route("/jieba1")
def jieba1():
    return render_template("Generation_Two/D3Chart.html")


@app.route("/D3Chart")
def D3Chart():

    return render_template("Generation_Two/D3test.html" )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True, processes=1)
