from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Sample data; usually fetched from a database
    videos = [
        {"title": "Video 1", "url": "video1.mp4"},
        {"title": "Video 2", "url": "video2.mp4"}
    ]
    threads = [
        {"title": "Discussion 1"},
        {"title": "Discussion 2"}
    ]
    return render_template('main.html', videos=videos, threads=threads)