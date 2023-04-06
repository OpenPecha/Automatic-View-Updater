import shutil
from pathlib import Path
from collection.views.plain_text import PlainTextView
from automatic_view_updater.generate_view import BASE_PATH, generate_view


def test_view():

    expected_view = Path("./tests/data/expected_result.txt").read_text(encoding="utf-8")
    result_views_path = generate_view("I3D4F1804",PlainTextView(),Path("./data"))
    first_view = result_views_path[0]
    result_view = first_view.read_text(encoding="utf-8")
    assert expected_view == result_view
    shutil.rmtree(BASE_PATH.as_posix())
