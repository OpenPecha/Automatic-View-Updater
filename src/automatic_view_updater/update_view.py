from generate_view import generate_view
from openpecha.utils import load_yaml
from pathlib import Path
from github import Github
import os
import logging



GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
OWNER="Openpecha-Data"

logging.basicConfig(
    filename="basefile_metadata.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)

def notifier(msg):
    logging.info(msg)

def extract_pecha_ids(msg):
    pecha_ids = [i.strip() for i in msg.split(",")]
    return pecha_ids


def update_repo(g, repo_name, file_path, commit_msg, new_content):
    try:
        repo = g.get_repo(f"{OWNER}/{repo_name}")
        contents = repo.get_contents(f"{file_path}", ref="master")
        repo.update_file(contents.path, commit_msg, new_content, sha=contents.sha, branch="master")
        notifier( f'{repo_name} updated ')
    except Exception as e:
        notifier( f'{repo_name} not updated with error {e}')

    
def push_view(pecha_id,view_path,view_type):
    g = Github(GITHUB_TOKEN)
    view = view_path.read_text(encoding="utf-8")
    base_id = view_path.stem
    view_name = f"{pecha_id}_{base_id}.txt"
    file_path = f"{collection_id}.opc/views/{view_type}/{view_name}"
    commit_msg = f"Updated {view_name}"
    update_repo(g, pecha_id, file_path, commit_msg, view)


def push_views(pecha_id,views_path,view_type):
    for view_path in views_path:
        push_view(pecha_id,view_path,view_type)


def get_view_types(pecha_id):
    meta_path = Path(f"./{collection_id}.opc/meta.yml")
    view_types = meta_path["item_views_map"]
    return view_types[pecha_id]

def get_collection_id():
    dirs = os.listdir(os.getcwd())
    for dir in dirs:
        if dir.endswith(".opc"):
            collection_id = Path(dir).stem
            return collection_id


def main(issue_message):
    global collection_id
    pecha_ids = extract_pecha_ids(issue_message)
    collection_id = get_collection_id()
    
    for pecha_id in pecha_ids:
        view_types = get_view_types(pecha_id)
        for view_type in view_types:
            views_path = generate_view(pecha_id,view_type)
            push_views(pecha_id,views_path,view_type)