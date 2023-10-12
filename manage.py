#!/usr/bin/env python3
# for creating commandlines
from flask.cli import FlaskGroup
from src import app

# create a cli group
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()