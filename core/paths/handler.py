from modules import FileManager
from .list import *
from . import list as l


def paths_handler():
    check_exists = [
        l.DOTPUSHER_DIR,
        l.JSONC_CONFIG,
    ]

    try:
        for i in check_exists:
            if not i.exists():
                Fm = FileManager(i)
                Fm.if_not_exists_create()

    except Exception as e:
        print(f"Path handler: {e}")
