import tiny
from flask import Flask, render_template, request

my_index = tiny.Index("../large-sample")
app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/search")
def search():
    q = request.args["q"]
    return render_template("results.html", q=q, results=my_index.search(q))
