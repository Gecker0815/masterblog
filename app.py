from flask import Flask, redirect, request, render_template
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)