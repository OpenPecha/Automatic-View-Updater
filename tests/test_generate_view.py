import shutil
from pathlib import Path

from automatic_view_updater.generate_view import BASE_PATH, generate_view
from automatic_view_updater.update_view import get_view_class


def test_view():

    expected_view = Path("./tests/data/expected_result.txt").read_text(encoding="utf-8")
    view = get_view_class("plaintext")
    result_views_path = generate_view("I3D4F1804", view())
    result_view = result_views_path[0].read_text(encoding="utf-8")
    assert expected_view == result_view
    shutil.rmtree(BASE_PATH.as_posix())
