from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data to mimic posts
posts = [
    {
        'id': 1,
        'title': 'My First Video',
        'content': 'This is a cool video about tech.',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
    },
    {
        'id': 2,
        'title': 'Second Tech Talk',
        'content': 'Exploring the latest in technology.',
        'video_url': 'https://www.youtube.com/embed/tgbNymZ7vqY'
    }
]

next_id = 3

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', posts=posts)

@app.route('/create', methods=['POST'])
def create_post():
    global next_id
    title = request.form['title']
    content = request.form['content']
    video_url = request.form['video_url']
    posts.append({'id': next_id, 'title': title, 'content': content, 'video_url': video_url})
    next_id += 1
    return redirect(url_for('home'))

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    global posts
    posts = [post for post in posts if post['id'] != post_id]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
