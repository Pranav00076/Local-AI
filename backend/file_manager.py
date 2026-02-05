import os, shutil
from .config import DATA_DIR

def save_upload(file):
    path = os.path.join(DATA_DIR, file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

def delete_file(name):
    os.remove(os.path.join(DATA_DIR, name))
