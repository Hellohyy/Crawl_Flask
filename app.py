from flask import Flask, render_template, redirect, request
from nltk.corpus import wordnet as wn
import nltk

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect("/search")


@app.route("/search")
def search():
    nltk.download()
    wanted = request.args.get("wanted", type=str)
    if not wanted:
        wanted = "home"

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
        # print(wordnote)

    return render_template('index.html', wordnet=wordnote, wordnetedgs=wordpath)


if __name__ == '__main__':
    app.run()
