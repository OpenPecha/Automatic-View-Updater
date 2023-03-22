from collection.views.plain_base import PlainBaseViewSerializer
from collection.items.pecha import Pecha,PechaMeta
from pathlib import Path
from git import Repo
from openpecha.core.pecha import OpenPechaFS
from openpecha.utils import load_yaml
import re


OPENPECHA_DATA_PREFIX_URL = "https://github.com/OpenPecha-Data"
OUTPUT_ROOT_PATH = "data"


def download_repo(item_id):
    item_path = OUTPUT_ROOT_PATH+"/"+item_id
    item_github_url = f"{OPENPECHA_DATA_PREFIX_URL}/{item_id}"
    Repo.clone_from(item_github_url,item_path)
    return item_path

def get_item(item_id):
    repo_path = download_repo(item_id)
    return repo_path

def get_item_meta(item_id,item_path):
    meta = None
    if re.match("^I",item_id):
        meta_path = Path(f"{item_path}/{item_id}.opf/meta.yml")
        meta = load_yaml(meta_path)
    return meta

def get_pecha_attr(dic,item_path):
    pecha = {}
    pecha_attrs = PechaMeta.__annotations__.keys()
    for pecha_attr in pecha_attrs:
        if pecha_attr in dic.keys():
            pecha[pecha_attr] = dic[pecha_attr]
        else:
            pecha[pecha_attr] = None
    pecha["pecha_path"] = item_path
    return pecha

def generate_view(item_id,output_dir):
    item_path = get_item(item_id)
    meta = get_item_meta(item_id,item_path)
    pecha_attr = get_pecha_attr(meta,item_path)
    pecha = PechaMeta(**pecha_attr)
    serializer = PlainBaseViewSerializer()
    serializer.serialize(pecha=pecha,output_dir=output_dir)


if __name__ == "__main__":
    generate_view("I3D4F1804","./data")