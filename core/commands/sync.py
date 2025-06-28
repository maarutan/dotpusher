from ..prepare_dir import PrepareDir


class Sync:
    def __init__(self):
        self.pdir = PrepareDir()

    def sync(self):
        self.pdir.walk_and_copy_on_dir("sync dotfiles ^^")
