from pathlib import Path
from src.automatic_view_updater.generate_view import generate_view

def test_view():
    expected_view = Path("tests/data/I3CN3916.txt").read_text(encoding="utf-8")
    result_views_path = generate_view("I3D4F1804","./data") 
    result_view = result_views_path[0].read_text(encoding="utf-8")
    assert expected_view == result_view