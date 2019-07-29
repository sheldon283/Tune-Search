#!/usr/bin/python3

from flask import Flask, render_template, request

import search
import sys

application = app = Flask(__name__)
app.debug = True

@app.route('/search', methods=["GET"])
def dosearch():
    query = request.args['query']
    qtype = request.args['query_type']

    """
    TODO:
    Use request.args to extract other information
    you may need for pagination.
    """
    search_results, size = search.search(query, qtype, int(request.args['pagenum']))
    am_pages = (size/20 + 1) if size % 20 != 0 else size/20
    print(am_pages, file = sys.stderr)
    print(size, file=sys.stderr)
    
    return render_template('results.html',
            query=query,
            query_type=qtype,
            results=len(search_results),
            search_results=search_results,
            size=size,
            amount_pages=am_pages,
            pagenum=int(request.args['pagenum']),
            )

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        pass
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
