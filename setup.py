from setuptools import setup, find_packages
import io
import os

VERSION = "0.1"


def get_long_description():
    with io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="markdown-to-sqlite",
    description="CLI tool for loading markdown files into a SQLite database",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    version=VERSION,
    license="Apache License, Version 2.0",
    packages=find_packages(),
    install_requires=["yamldown", "markdown", "sqlite-utils", "click"],
    entry_points="""
        [console_scripts]
        markdown-to-sqlite=markdown_to_sqlite.cli:cli
    """,
    url="https://github.com/simonw/markdown-to-sqlite",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Database",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
