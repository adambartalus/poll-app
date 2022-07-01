from flask.cli import FlaskGroup
import click

from poll import create_app
from poll.extensions import db

cli = FlaskGroup(create_app())


@cli.command("create-db")
def create_db():
    """Creates the db tables."""
    db.create_all()
    click.echo('Initialized the database.')


@cli.command("drop-db")
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == "__main__":
    cli()
