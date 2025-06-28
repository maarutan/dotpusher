from os import getcwd, chdir, environ
from pathlib import Path
from sys import exit
from ..prepare_dir import PrepareDir
from modules import Git, StylizedText


class Push:
    def __init__(self):
        self.g = Git()
        self.pdir = PrepareDir()
        self.styt = StylizedText
        self.confh = self.pdir.confh
        self.col = self.pdir.col
        self.p = self.pdir.p
        self.fm = self.pdir.fm
        self.result_dir = self.pdir.result_dir

    def push(self, force: bool = False):
        print(f"\n{self.styt(col=self.col.PURPLE.value, content='dotpusher')}")

        self.result_dir = Path(self.result_dir).resolve()
        is_git_repo = self.pdir.is_git()

        if is_git_repo:
            self.pdir.rm_all_without_git(
                True
            ) if force else self.pdir.walk_and_copy_on_dir("replace dotfiles ^^", True)

        else:
            if self.result_dir.exists():
                self.fm(self.result_dir).delete()

            self.fm(self.result_dir).if_not_exists_create()

            clone_success = self.g.clone(self.confh.get_url(), self.result_dir)
            if not clone_success:
                print(f"[fatal] Git clone failed. Aborting.")
                exit(1)

        if force:
            self.pdir.rm_all_without_git(self.pdir.is_git())
            self.pdir.walk_and_copy_on_dir("copy for push dotfiles ^^")

        self.g.add(self.result_dir)
        self.g.commit(
            self.result_dir,
            message=self.confh.get_default_commit_message(),
            noconfirm=self.confh.get_noconfirm(),
        )
        self.g.push(chdir=self.result_dir, branch=self.confh.get_branch())
