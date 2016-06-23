#!/usr/bin/env python3
import requests
from flask import *
import random

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
scheduler = BackgroundScheduler()
url = "https://reddit.com/r/gonewild/comments.json?limit=200"
comments = []

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

def update_comments():
    global comments
    data = requests.get(url, headers={"User-Agent": "/u/suudo http://compliment.b303.me (comments from gonewild)"}).json()
    comments = [a["data"]["body"] for a in data["data"]["children"]]

@app.route("/")
def compliment():
    if request_wants_json():
        return jsonify({"compliment": random.choice(comments)})
    return random.choice(comments)

@app.route("/comments")
def all():
    if request_wants_json():
        return jsonify({"comments": comments})
    return "<ul>\n" + "\n".join("<li>{}</li>\n".format(c) for c in comments) + "</ul>"

update_comments()
scheduler.add_job(update_comments, 'interval', minutes=15)
scheduler.start()
if __name__ == "__main__":
    try:
        app.run(port=56735, debug=True)
    finally:
        scheduler.shutdown()
