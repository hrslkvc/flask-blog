def get_many():
    query = """
        SELECT p.*, u.username as author_name
        FROM posts p JOIN users u ON p.author_id = u.id
        ORDER BY created DESC
        """


def get_one(post_id):
    query = "SELECT p.*, u.username as author_name FROM posts p JOIN users u ON p.author_id = u.id WHERE p.id = ?"


def create(data):
    pass


def update(post_id, data):
    pass


def delete(post_id):
    pass


def get_many_by_author(username):
    query = "SELECT p.*, u.username as author_name FROM posts p JOIN users u ON p.author_id = u.id WHERE author_id = ?"
