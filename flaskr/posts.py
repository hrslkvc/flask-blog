import os

from flask import Blueprint, render_template, request, redirect, url_for, g, abort, current_app
from werkzeug.utils import secure_filename

from .auth import login_required
from .db import get_db
from .services import post_service

bp = Blueprint('posts', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    posts = post_service.get_many()

    return render_template('posts/index.html', posts=posts)


@bp.route('/posts/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        image = request.files['image']
        filename = secure_filename(image.filename)
        db = get_db()
        db.execute("INSERT INTO posts (title, body, author_id, image) values (?, ?, ?, ?)",
                   (request.form['title'], request.form['body'], g.user['id'], filename))
        db.commit()

        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('posts.index'))

    return render_template('posts/create.html')


@bp.route('/posts/<post_id>')
def show(post_id):
    post = post_service.get_one(post_id)

    if not post:
        abort(404)

    return render_template('posts/show.html', post=post)


@bp.route('/author/<username>')
def by_author(username):
    posts = post_service.get_many_by_author(username)
    return render_template('posts/index.html', posts=posts)
