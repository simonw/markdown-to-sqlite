# markdown-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/markdown-to-sqlite.svg)](https://pypi.python.org/pypi/markdown-to-sqlite)
[![Tests](https://github.com/simonw/markdown-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/markdown-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/markdown-to-sqlite/blob/main/LICENSE)

CLI tool for loading markdown files into a SQLite database.

YAML embedded in the markdown files will be used to populate additional columns.

    Usage: markdown-to-sqlite [OPTIONS] PATHS... DBNAME TABLE

For example:

    $ markdown-to-sqlite file1.md file2.md docs.db documents
