from pathlib import Path
from automatic_view_updater.generate_view import generate_view
import tempfile

def test_view():
    f = tempfile.TemporaryDirectory(dir = "./data")
    expected_view = Path("./tests/data/expected_result.txt").read_text(encoding="utf-8")
    result_views_path = generate_view("I3D4F1804",f.name) 
    result_view = result_views_path[0].read_text(encoding="utf-8")
    assert expected_view == result_view
    f.cleanup()