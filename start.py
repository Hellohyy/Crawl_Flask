from flask import Flask, redirect, url_for, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
import config
from models import first_crawl, second_crawl
from crawl import c_start_crawl1
from crawl2 import c_start_crawl2, c_start_crawl2_images
from pyecharts.charts import WordCloud
from nltk.corpus import wordnet as wn
from urllib.request import Request, urlopen
import threading
import time
from multiprocessing import Process
import jieba, random
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json
import networkx as nx  # 导入NetworkX包

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


@app.route("/D3ForceData")
def D3ForceData():
    nodes = []  # 所有节点
    edges = []  # 所有边

    # 电影、导演、演员为节点
    all_films = []
    all_directors = []
    all_actors = []

    with open("./static/dbmovies.json", 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        # print(load_dict, "\n\n")

    # for i in range(len(load_dict)):
    for i in range(40):
        film_directors = load_dict[i]["director"]
        film_actors = load_dict[i]["actor"]
        # print(i)

        all_films.append(load_dict[i]["title"])
        if film_directors is not None:
            for director in film_directors:
                if director not in all_directors:
                    all_directors.append(director)

        count = 0
        if film_actors is not None:
            for actor in film_actors:
                if count < 30:
                    if actor not in all_actors:
                        all_actors.append(actor)
                        count += 1

    print("电影总数:", len(all_films), "| 导演总数:", len(all_directors), "|演员总数:", len(all_actors))

    # 把所有节点加入nodes
    count = 0
    for film in all_films:
        nodes.append({'name': film, 'class': 'film', 'group': 0, 'size': 16, "index": count})
        count += 1
    for director in all_directors:
        nodes.append({'name': director, 'class': 'director', 'group': 1, 'size': 10, "index": count})
        count += 1
    for actor in all_actors:
        nodes.append({'name': actor, 'class': 'actor', 'group': 2, 'size': 5, "index": count})
        count += 1

    # print(nodes, "\n节点总数:", len(nodes))
    with open("./static/dbmovies_result.json", "w", encoding='utf-8') as f:
        json.dump(nodes, f, ensure_ascii=False)

    edges = []
    node_num = 0
    for node in nodes:
        if node["class"] is "film":
            file = {}
            for dic in load_dict:
                if node["name"] is dic["title"]:
                    film = dic
                    for i in range(len(nodes)):
                        if nodes[i]["name"] in film["director"]:
                            edges.append({'source': i, "target": node_num, "value": 3,"relation": "导演"})
                        if nodes[i]["name"] in film["actor"]:
                            edges.append({'source': i, "target": node_num, "value": 2, "relation": "出演"})
        else:
            break
        node_num += 1

    # edges.append({'source': 1, "target": 2, "value": 3, "relation": ""})

    with open("./static/dbmovies_result_edges.json", "w", encoding='utf-8') as f:
        json.dump(edges, f, ensure_ascii=False)

    da = {}
    da["nodes"] = nodes
    da["links"] = edges
    with open("./static/dbmovies_result_datas.json", "w", encoding='utf-8') as f:
        json.dump(da, f, ensure_ascii=False)

    # return render_template("Generation_Two/D3Force.html", nodes=nodes)
    return "yes"


@app.route("/D3ForceData2")
def D3ForceData2():
    with open("./static/dbmovies_result.json", 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)

    with open("./static/dbmovies_result_edges.json", 'r', encoding='utf-8') as load_e:
        load_dict_edges = json.load(load_e)

    datas = {}
    nodes = []
    links = []

    G = nx.Graph()  # 建立一个空的无向图G

    for i in range(len(load_dict)):
        nodes.append(load_dict[i])
        G.add_node(i) # 添加一个节点1

    for i in range(len(load_dict_edges)):
        links.append(load_dict_edges[i])
        G.add_edge(load_dict_edges[i]["target"], load_dict_edges[i]["source"] )

    datas["nodes"] = nodes
    datas["links"] = links

    # print(G.nodes())# 输出全部的节点： [1, 2, 3]
    # //print(G.edges())  # 输出全部的边：[(2, 3)]
    print(G.number_of_edges())  # 输出边的数量：1

    print(nx.average_clustering(G))
    print(nx.pagerank(G)[0])

    # hub, authority = nx.hits(G)
    # print(hub)
    # print(authority)
    # print(nx.clustering(G))
    # print(nx.degree(G))
    # print(nx.degree(G)[0])

    degree_will_sort = {}
    degree_num = []  # 度的数目
    degree_count = [] # 度数目对应的数量
    for num in nx.degree(G):
        degree_will_sort[str(num[0])] = num[1]
        if num[1] not in degree_num:
            degree_num.append(num[1])
            degree_count.append(1)
        else:
            degree_count[degree_num.index(num[1])] += 1

    print(degree_num)
    print(degree_count)
    # 节点边排序
    degree_sort = sorted(degree_will_sort.items(), key=lambda degree_will_sort:degree_will_sort[1], reverse=True)

    return render_template("Generation_Two/D3Force2.html", datas=json.dumps(datas, ensure_ascii=False), cluster=nx.clustering(G), pagerank=nx.pagerank(G), degree=nx.degree(G))
    # return render_template("Generation_Two/D3Force.html", nodes=nodes)
    # return render_template("Generation_Two/D3Force2.html", datas=json.dumps(datas, ensure_ascii=False))


@app.route("/Wordnet")
def Wordnet():
    wanted = request.args.get("wanted", type=str)
    if not wanted:
        wanted = "education"

    wordnote = []
    wordpath = []
    snumber = 0
    tnumber = 0
    print(wn.synsets(wanted))  # 打印home的多个词义
    for n in wn.synsets(wanted):
        # print(n.lemma_names())
        # wordnote = [{d['name']} for d in n.lemma_names()]
        for wordn in n.lemma_names():
            notes = {}
            paths = {}
            notes['name'] = wordn
            paths['source'] = snumber
            paths['target'] = tnumber
            wordnote.append(notes)
            wordpath.append(paths)
            # print(notes)
            tnumber += 1
        snumber += 1
    return render_template('Generation_Two/index3.html', wordnet=wordnote, wordnetedgs=wordpath)


# 西游记
@app.route("/Xiyouji")
def Xiyouji():
    # import pandas as pd  # 导入pandas包
    # data = pd.read_csv("train.csv")
    import csv

    sFileName = './static/triples.csv'

    nds_name =[]
    nds = []
    liks = []
    ro = []
    with open(sFileName, newline='', encoding='UTF-8') as csvfile:
        rows = csv.reader(csvfile)
        count = 0
        for row in rows:
            if count is not 0:
                if row[0] not in nds_name:
                    nds_name.append(row[0])
                if row[1] not in nds_name:
                    nds_name.append(row[1])
                ro.append(row)
            count += 1
    lead = ["唐僧", "孙悟空", "猪八戒", "沙僧", "白龙马"]
    person = ["陈光蕊", "殷温娇", "法明和尚", "李世民", "殷开山", "卵二姐", "高翠兰", "李渊", "李建成", "李元吉", "王珪", "秦琼", "萧瑀", "傅奕","魏征",
              "李玉英", "房玄龄", "杜如晦", "徐世绩", "徐茂公", "许敬宗", "马三宝", "段志贤", "程咬金", "虞世南", "张道源", "张士衡", "高太公", "高香兰",
              "高玉兰", "寇洪", "寇梁", "袁守诚", "李靖","袁天罡","宼栋"
              ]
    monster = ["牛魔王", "蛟魔王", "鹏魔王", "狮驼王", "猕猴王", "禺狨王", "红孩儿", "黑风怪", "黄风怪", "黄毛貂鼠", "金角", "银角", "铁扇公主",
                "九尾狐狸", "西海龙王太子", "鼍龙怪", "灵感大王", "独角兕大王", "玉面公主", "金毛犼", "黄眉道童", "百眼魔君", "青狮", "白象",
               "大鹏金翅雕", "九头狮子", "玉兔精", "白鹿精", "黄眉大王","敖摩昂","敖闰","狐阿七"

               ]
    immoral = ["金蝉子", "菩提老祖", "镇元子", "天蓬元帅", "卷帘大将", "西海龙王", "西海龙母", "敖摩昂太子", "西海龙女", "正元龙",
               "木吒", "二十四路诸天", "守山大神", "善财童子", "捧珠龙女", "金吒", "观音菩萨", "如来", "灵吉菩萨", "太上老君",
               "弥勒佛", "毗蓝婆菩萨", "文殊菩萨", "普贤菩萨", "哪吒", "嫦娥", "昴日星官", "嫦娥",	"后羿","太乙救苦天尊","南极寿星","东来佛祖笑和尚"
               ]

    aaa = ["唐僧", "孙悟空", "猪八戒", "沙僧", "白龙马","陈光蕊", "殷温娇", "法明和尚", "李世民", "殷开山", "卵二姐", "高翠兰", "李渊", "李建成", "李元吉", "王珪", "秦琼", "萧瑀", "傅奕","魏征",
              "李玉英", "房玄龄", "杜如晦", "徐世绩", "徐茂公", "许敬宗", "马三宝", "段志贤", "程咬金", "虞世南", "张道源", "张士衡", "高太公", "高香兰",
              "高玉兰", "寇洪", "寇梁", "袁守诚", "李靖","袁天罡","牛魔王", "蛟魔王", "鹏魔王", "狮驼王", "猕猴王", "禺狨王", "红孩儿", "黑风怪", "黄风怪", "黄毛貂鼠", "金角", "银角", "铁扇公主",
                "九尾狐狸", "西海龙王太子", "鼍龙怪", "灵感大王", "独角兕大王", "玉面公主", "金毛犼", "黄眉道童", "百眼魔君", "青狮", "白象",
               "大鹏金翅雕", "九头狮子", "玉兔精", "白鹿精", "黄眉大王","敖摩昂","敖闰","金蝉子", "菩提老祖", "镇元子", "天蓬元帅", "卷帘大将", "西海龙王", "西海龙母", "敖摩昂太子", "西海龙女", "正元龙",
               "木吒", "二十四路诸天", "守山大神", "善财童子", "捧珠龙女", "金吒", "观音菩萨", "如来", "灵吉菩萨", "太上老君",
               "弥勒佛", "毗蓝婆菩萨", "文殊菩萨", "普贤菩萨", "哪吒", "嫦娥", "昴日星官", "嫦娥",	"后羿"]
    G = nx.Graph()  # 建立一个空的无向图G
    for i in range(len(nds_name)):
        if nds_name[i] in lead:
           nds.append({'name': nds_name[i], 'class': "lead", 'group': 0, 'size': 20, "i": i})
        if nds_name[i] in person:
           nds.append({'name': nds_name[i], 'class': "person", 'group': 1, 'size': 12, "i": i})
        if nds_name[i] in monster :
           nds.append({'name': nds_name[i], 'class': "monster", 'group': 2, 'size': 8, "i": i})
        if nds_name[i] in immoral:
           nds.append({'name': nds_name[i], 'class': "immoral", 'group': 3, 'size': 8, "i": i})
        G.add_node(i)  # 添加一个节点1

    print("人物数:", len(nds_name))
    print("节点数:", len(nds))
    notin_nds = []

    for row in ro:
        for nd in nds:
            if nd["name"] is row[0]:
                source = nd["i"]
            if nd["name"] is row[1]:
                target = nd["i"]
        liks.append({'source': source, "target": target, "value": 2, "relation": row[3]})
        G.add_edge(source, target)

    da = {}
    da["nodes"] = nds
    da["links"] = liks
    with open("./static/Xiyouji_result_datas.json", "w", encoding='utf-8') as f:
        json.dump(da, f, ensure_ascii=False)

    # print(G.nodes())  # 输出全部的节点： [1, 2, 3]
    # print(G.edges())  # 输出全部的边：[(2, 3)]
    # print(G.number_of_edges())  # 输出边的数量：1
    #
    # print(nx.average_clustering(G))
    # print(nx.clustering(G))
    return "Yes"


@app.route("/XiyoujiD3")
def XiyoujiD3():
    da = {}
    return render_template("Generation_Two/Xiyouji.html", datas=json.dumps(da, ensure_ascii=False))


import networkx as nx


@app.route("/GenerateWSNet")
def GenerateWSNet():
    # 请输入网络节点总数NETWORK_SIZE
    # NETWORK_SIZE = int(input())
    NETWORK_SIZE = 200
    # 请输入规则网络要连的邻接个数k
    k = 4
    # 请输入重连概率p
    p = float(0.4)
    ws = nx.watts_strogatz_graph(NETWORK_SIZE, k, p)
    ps = nx.circular_layout(ws)  # 布置框架
    nx.draw(ws, ps, with_labels=False, node_size=30)
    plt.show()
    return "Generate Success!"


@app.route("/GenerateBANet")
def GenerateBANet():
    BA = nx.barabasi_albert_graph(200, 2)
    ps = nx.spring_layout(BA)   # 布置框架
    nx.draw(BA, ps, with_labels=False, node_size=30)
    plt.show()
    return "Generate Success!"


@app.route("/football")
def search():
    nodes = []
    links = []
    MDG = nx.read_pajek('./static/football.net');
    G = nx.DiGraph(MDG)
    gn = G.nodes()
    cluster = nx.clustering(G)
    pagerank = nx.pagerank(G)
    hub, authority = nx.hits(G)
    lgn = list(gn)
    print(G)
    for u in gn:
        node = {}
        node['name'] = u
        node['intro'] = '该节点的聚集系数为：'+str(format(cluster[u],'.3f'))+"<br>"+\
                        '该节点的pagerank为：'+str(format(pagerank[u],'.3f'))+"<br>"+\
                        '该节点的权威值为：'+str(format(authority[u],'.3f'))+"<br>"+ \
                        '该节点的中枢值为：' + str(format(hub[u], '.3f'))
        nodes.append(node)
    for u, v in G.edges():
        link = {}
        link['source'] = lgn.index(u)
        link['target'] = lgn.index(v)
        links.append(link)
    return render_template('Generation_Two/football.html',nodes = nodes,links = links)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True, processes=1)
