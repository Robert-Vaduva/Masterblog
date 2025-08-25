import os
from flask import Flask, render_template, request, redirect, url_for
import helpers.json.json_helper as json_helper


app = Flask(__name__)
PATH = os.path.join("data", "blog_posts.json")


@app.route('/')
def index():
    blog_posts = json_helper.read_json_data(PATH)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # We will fill this in the next step
        blog_posts = json_helper.read_json_data(PATH)
        id = blog_posts[-1]["id"] + 1
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        blog_posts.append({"id": id, "author": author, "title": title, "content": content})
        json_helper.write_json_data(PATH, blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
