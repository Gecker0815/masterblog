from flask import Flask, redirect, request, render_template, url_for
from storage import Storage

app = Flask(__name__)
data = Storage()

@app.route('/')
def index():
    blog_posts = data.list_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        try:
            data.add({
                "author": author,
                "title": title,
                "content": content
            })
            return redirect('/')
        except ValueError as e:
            return f"<p>Error: {e}</p>"

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    try:
        data.delete(post_id)
        return redirect('/')
    except ValueError as e:
        return f"<p>Error: {e}</p>"

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = data.read(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form.get('title') or post['title']
        content = request.form.get('content') or post['content']

        data.update(post_id, title, content)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['GET', 'POST'])
def like(post_id):
    data.like(post_id, 1)
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)