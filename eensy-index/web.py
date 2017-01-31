from flask import Flask, render_template, request
import eensy

app = Flask(__name__)

search_index = eensy.Index("../large-sample")

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/search")
def query(*args, **kwargs):
    q = request.args["q"]
    results = search_index.search(q)
    return render_template("results.html", q=q, results=results)
