import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@click.command('db_create_all')
@with_appcontext
def db_create_all():
    db.drop_all()
    # db.create_all()
