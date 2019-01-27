import click
from pathlib import Path
import sqlite3
from sqlite_utils import Database
import yamldown
import markdown
import hashlib


@click.command()
@click.version_option()
@click.argument("paths", type=click.Path(exists=True), nargs=-1, required=True)
@click.argument("dbname", nargs=1)
@click.argument("table", nargs=1)
def cli(paths, dbname, table):
    """
    Load markdown files into a SQLite database
    
    https://github.com/simonw/markdown-to-sqlite
    """
    db = Database(dbname)
    md = markdown.Markdown()
    docs = []
    for path in paths:
        metadata, text = yamldown.load(open(path))
        html = md.convert(text)
        doc = {
            "_id": str(path),
            "text": text,
            "html": html,
            **metadata,
        }
        docs.append(doc)
    db[table].upsert_all(docs, pk="_id")
