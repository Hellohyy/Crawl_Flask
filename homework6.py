
from flask import Flask, render_template, request
from werkzeug.utils import redirect

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    return redirect("/search")

import networkx as nx


@app.route("/search")
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
    return render_template('index.html',nodes = nodes,links = links)


if __name__=='__main__':
    app.run(host='0.0.0.0',port='5002')
