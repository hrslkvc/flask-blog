from flask import Blueprint, render_template

from .auth import login_required
from .db import get_db

bp = Blueprint('posts', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    db = get_db()
    posts = db.execute('SELECT * FROM posts')
    return render_template('posts/index.html', posts=posts)


@bp.route('/posts/create')
def create():
    return render_template('posts/create.html')
