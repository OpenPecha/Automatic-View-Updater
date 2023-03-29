import re
from pathlib import Path

from collection.items.pecha import Pecha
from collection.views.view import View
from git import Repo
from openpecha.config import BASE_PATH
from openpecha.utils import load_yaml

OPENPECHA_DATA_PREFIX_URL = "https://github.com/OpenPecha-Data"
DEFAULT_OUTPUT_DIR = BASE_PATH


def download_repo(item_id, output_dir):
    item_path = output_dir.as_posix() + "/" + item_id
    item_github_url = f"{OPENPECHA_DATA_PREFIX_URL}/{item_id}"
    Repo.clone_from(item_github_url, item_path)
    return item_path


def get_item(item_id, output_dir):
    repo_path = download_repo(item_id, output_dir)
    return repo_path


def get_item_meta(item_id, item_path):
    meta = None
    if re.match("^I", item_id):
        meta_path = Path(f"{item_path}/{item_id}.opf/meta.yml")
        meta = load_yaml(meta_path)
    return meta


def get_pecha_attr(dic, item_path):
    pecha = {}
    pecha_attrs = Pecha.__annotations__.keys()
    for pecha_attr in pecha_attrs:
        if pecha_attr in dic.keys():
            pecha[pecha_attr] = dic[pecha_attr]
        else:
            pecha[pecha_attr] = None
    pecha["pecha_path"] = item_path
    return pecha


def generate_view(item_id: str, view: View, output_dir: Path = None):
    if output_dir:
        output_dir = BASE_PATH
    item_path = get_item(item_id, output_dir)
    meta = get_item_meta(item_id, item_path)
    pecha_attr = get_pecha_attr(meta, item_path)
    pecha = Pecha(**pecha_attr)
    views_path = view.serialize(pecha=pecha, output_dir=BASE_PATH)
    return views_path


if __name__ == "__main__":
    generate_view("I3D4F1804", Path("./data"))
