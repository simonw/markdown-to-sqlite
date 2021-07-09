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

THREE = """
---
abstract: Third abstract
accepted: false
date: 2021-07-09 10:45:00
presenters:
- twitter: ryancheley
  website: https://ryancheley.com/
---


# Trial 1

  Method           Start                                                                                                                                                             Dirty                                                                                                                                                             Cleaned
  ---------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
  Water            ![Trial1_Start_Water](/images/uploads/2016/12/Trial1_Start_Water-300x300.jpg){.alignnone .size-medium .wp-image-139 width="300" height="300"}          ![Trial1_Dirty_Water](/images/uploads/2016/12/Trial1_Dirty_Water-300x300.jpg){.alignnone .size-medium .wp-image-136 width="300" height="300"}          ![Trial1_Clean_Water](/images/uploads/2016/12/Trial1_Clean_Water-300x300.jpg){.alignnone .size-medium .wp-image-156 width="300" height="300"}
------------------------------------------------------------------------

"""



def test_basic(tmpdir):
    (tmpdir / "one.md").write(ONE)
    (tmpdir / "two.md").write(TWO)
    (tmpdir / "three.md").write(THREE)
    result = CliRunner().invoke(
        cli.cli,
        [
            str(tmpdir / "info.db"),
            "talks",
            str(tmpdir / "one.md"),
            str(tmpdir / "two.md"),
            str(tmpdir / "three.md"),
        ],
    )
    db = Database(str(tmpdir / "info.db"))
    assert ["talks"] == db.table_names()
    assert 3 == db["talks"].count
    one, two, three = db.execute_returning_dicts("select * from talks")
    
    # Test row 1
    assert (
        "<h1>Heading</h1>\n<p>Text</p>\n<ul>\n<li>list</li>\n<li>list</li>\n</ul>"
        == one["html"]
    )
    assert "This is an abstract" == one["abstract"]
    assert [
        {"twitter": "simonw", "website": "https://simonwillison.net/"},
        {"twitter": "natbat", "website": "http://blog.natbat.net/"},
    ] == json.loads(one["presenters"])
    assert 1 == one["accepted"]
    assert "2018-10-14T09:00:00" == one["date"]

    # Test row 2
    assert "<h1>Heading 2</h1>" == two["html"]
    assert "Second abstract" == two["abstract"]
    assert [{"twitter": "cleopaws"}] == json.loads(two["presenters"])
    assert 0 == two["accepted"]
    assert "2018-11-14T09:00:00" == two["date"]
    
    # test row 3
    assert "Third abstract" == three["abstract"]
    assert [
        {"twitter": "ryancheley", "website": "https://ryancheley.com/"},
    ] == json.loads(three["presenters"])
    assert 0 == three["accepted"]
    assert "2021-07-09T10:45:00" == three["date"]
    assert 'Start' in three["html"]
    assert 'Dirty' in three["html"]
    assert 'Cleaned' in three["html"]
    assert 'Water' in three["html"]
    assert 'Method' in three["html"]
    assert 'images' in three["html"]