"""
Flask Blog Application
----------------------

This module implements a simple blog application using the Flask web framework.
Blog posts are stored in a JSON file located under the `data/` directory.

Features:
    • View all blog posts on the homepage (`/`).
    • Add a new post using the ADD form (`/add`).
    • Delete an existing post by its ID (`/delete/<id>`).

Modules used:
    - os: for file path handling.
    - flask: for the web framework (routing, templates, requests, redirects).
    - helpers.json.json_helper: for reading and writing blog data in JSON format.

To run the application:
    $ python app.py

The application will start a development server on http://localhost:5000
"""


import os
from flask import Flask, render_template, request, redirect, url_for
import helpers.json.json_helper as json_helper


app = Flask(__name__)
PATH = os.path.join("data", "blog_posts.json")
FIRST_ID = 1
LIKES_AT_START = 0


@app.route('/')
def index():
    """Render the homepage with all blog posts."""
    blog_posts = json_helper.read_json_data(PATH)

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handle displaying the ADD form and saving a new blog post."""
    if request.method == 'POST':
        # read the existing posts
        blog_posts = json_helper.read_json_data(PATH)

        if blog_posts:  # not empty
            post_id = blog_posts[-1]["id"] + 1  # get the latest id and increment it
        else:
            post_id = FIRST_ID
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        blog_posts.append({"id": post_id, "author": author, "title": title,
                           "likes": LIKES_AT_START, "content": content})
        json_helper.write_json_data(PATH, blog_posts)

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Delete a blog post by its ID and redirect to the homepage."""
    # read the existing posts
    blog_posts = json_helper.read_json_data(PATH)
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break
    json_helper.write_json_data(PATH, blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Handle displaying and processing the update form for a blog post."""
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)

    if request.method == 'POST' and post:
        # Update the post in the JSON file
        blog_posts = json_helper.read_json_data(PATH)
        for blog in blog_posts:
            if blog['id'] == post_id:
                blog['author'] = request.form.get("author")
                blog['title'] = request.form.get("title")
                blog['content'] = request.form.get("content")
                break
        json_helper.write_json_data(PATH, blog_posts)
        # Redirect back to index
        return redirect(url_for('index'))

    if request.method == 'GET' and post:
        # So display the update.html page
        return render_template('update.html', post=post)

    # Post not found
    return "Post not found", 404


@app.route('/like/<int:post_id>')
def like(post_id):
    """Increment the like count for a blog post and redirect to index."""
    blog_posts = json_helper.read_json_data(PATH)
    for blog in blog_posts:
        if blog["id"] == post_id:
            blog["likes"] += 1
            break
    json_helper.write_json_data(PATH, blog_posts)
    return redirect(url_for('index'))


def fetch_post_by_id(post_id):
    """Return a blog post dictionary matching the given ID, or None if not found."""
    blog_posts = json_helper.read_json_data(PATH)
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
