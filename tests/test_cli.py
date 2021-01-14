from sqlite_utils import Database
from markdown_to_sqlite import cli
from click.testing import CliRunner
import json

ONE = """---
abstract: This is an abstract
accepted: true
date: 2018-10-14 09:00:00
presenters:
- twitter: simonw
  website: https://simonwillison.net/
- twitter: natbat
  website: http://blog.natbat.net/
---
# Heading

Text

* list
* list
"""

TWO = """
---
abstract: Second abstract
accepted: false
date: 2018-11-14 09:00:00
presenters:
- twitter: cleopaws
---
# Heading 2
"""


def test_basic(tmpdir):
    (tmpdir / "one.md").write(ONE)
    (tmpdir / "two.md").write(TWO)
    result = CliRunner().invoke(
        cli.cli,
        [
            str(tmpdir / "one.md"),
            str(tmpdir / "two.md"),
            str(tmpdir / "info.db"),
            "talks",
        ],
    )
    db = Database(str(tmpdir / "info.db"))
    assert ["talks"] == db.table_names()
    assert 2 == db["talks"].count
    one, two = db.execute_returning_dicts("select * from talks")
    assert (
        "<h1>Heading</h1>\n<p>Text</p>\n<ul>\n<li>list</li>\n<li>list</li>\n</ul>"
        == one["html"]
    )
    assert "<h1>Heading 2</h1>" == two["html"]
    assert "This is an abstract" == one["abstract"]
    assert "Second abstract" == two["abstract"]
    assert [
        {"twitter": "simonw", "website": "https://simonwillison.net/"},
        {"twitter": "natbat", "website": "http://blog.natbat.net/"},
    ] == json.loads(one["presenters"])
    assert [{"twitter": "cleopaws"}] == json.loads(two["presenters"])
    assert 1 == one["accepted"]
    assert 0 == two["accepted"]
    assert "2018-10-14T09:00:00" == one["date"]
    assert "2018-11-14T09:00:00" == two["date"]
