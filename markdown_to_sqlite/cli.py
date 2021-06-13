import click
from pathlib import Path
import sqlite3
from sqlite_utils import Database
import hashlib
import markdown
import yamldown


@click.command()
@click.version_option()
@click.argument("dbname", nargs=1)
@click.argument("table", nargs=1)
@click.argument("paths", type=click.Path(exists=True), nargs=-1, required=True)
def cli(paths, dbname, table):
    """
    Load markdown files into a SQLite database

    https://datasette.io/tools/markdown-to-sqlite
    """
    db = Database(dbname)
    md = markdown.Markdown()
    docs = []
    for path in paths:
        metadata, text = yamldown.load(open(path))
        html = md.convert(text)
        doc = {
            "_id": hashlib.sha1(path.encode("utf8")).hexdigest(),
            "_path": path,
            "text": text,
            "html": html,
            **(metadata or {}),
        }
        docs.append(doc)
    db[table].upsert_all(docs, pk="_id")
