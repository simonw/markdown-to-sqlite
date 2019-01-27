# markdown-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/markdown-to-sqlite.svg)](https://pypi.python.org/pypi/markdown-to-sqlite)
[![Travis CI](https://travis-ci.com/simonw/markdown-to-sqlite.svg?branch=master)](https://travis-ci.com/simonw/markdown-to-sqlite)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/markdown-to-sqlite/blob/master/LICENSE)

CLI tool for loading markdown files into a SQLite database.

YAML embedded in the markdown files will be used to populate additional columns.

This is in extremely early stages of development - very much a 0.1.

    Usage: markdown-to-sqlite [OPTIONS] PATHS... DBNAME TABLE

For example:

    $ markdown-to-sqlite file1.md file2.md docs.db documents