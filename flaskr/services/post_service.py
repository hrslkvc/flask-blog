from flaskr.db import get_db


def get_many():
    query = """
        SELECT p.*, u.username as author_name
        FROM posts p JOIN users u ON p.author_id = u.id
        ORDER BY created DESC
        """

    return get_db().execute(query).fetchall()


def get_one(post_id):
    query = "SELECT p.*, u.username as author_name FROM posts p JOIN users u ON p.author_id = u.id WHERE p.id = ?"

    return get_db().execute(query, (post_id,)).fetchone()


def create(data):
    pass


def update(post_id, data):
    pass


def delete(post_id):
    pass


def get_many_by_author(username):
    db = get_db()
    user = db.execute("SELECT id FROM users where username = ?", (username,)).fetchone()
    query = "SELECT p.*, u.username as author_name FROM posts p JOIN users u ON p.author_id = u.id WHERE author_id = ?"
    return get_db().execute(query, (user['id'],)).fetchall()
