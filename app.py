from flask import Flask, render_template
from storage import Storage

app = Flask(__name__)
data = Storage()

@app.route('/')
def index():
    blog_posts = data.list_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)