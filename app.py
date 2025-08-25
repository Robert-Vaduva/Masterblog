"""
Flask Blog Application
----------------------

This module implements a simple blog application using the Flask web framework.
Blog posts are stored in a JSON file located under the `data/` directory.

Features:
    • View all blog posts on the homepage (`/`).
    • Add a new post using the add form (`/add`).
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

        post_id = blog_posts[-1]["id"] + 1  # get the latest id and increment it
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        blog_posts.append({"id": post_id, "author": author, "title": title, "content": content})
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
            json_helper.write_json_data(PATH, blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Handle displaying and processing the update form for a blog post."""
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        # read the existing posts
        blog_posts = json_helper.read_json_data(PATH)
        for blog in blog_posts:
            if blog['id'] == post_id:
                blog['author'] = request.form.get("author")
                blog['title'] = request.form.get("title")
                blog['content'] = request.form.get("content")
        json_helper.write_json_data(PATH, blog_posts)
        # Redirect back to index
        return redirect(url_for('index'))

    # Else, it's a GET request
    if request.method == 'GET':
        # So display the update.html page
        return render_template('update.html', post=post)


def fetch_post_by_id(post_id):
    """Return a blog post dictionary matching the given ID, or None if not found."""
    blog_posts = json_helper.read_json_data(PATH)
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
