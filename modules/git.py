from pathlib import Path
from subprocess import CalledProcessError, run
import sys
from os import system, chdir
from .shell import Shell
from .colors import Col


class Git:
    def __init__(self) -> None:
        self.col = Col
        self.sh = Shell()

    def _formatted_output(
        self,
        command: str,
        *args,
    ) -> None:
        print(
            f"{self.col.YELLOW.value}~~>  {self.col.PURPLE.value}git{self.col.CYAN.value} {self.col.UNDERLINE_TEXT.value}{command} {' '.join(args)}{self.col.RESET.value}"
        )

    def change_dir_to_result(self, result_dir) -> None:
        if not result_dir.exists():
            raise RuntimeError(f"Result dir does not exist: {result_dir}")
        chdir(result_dir)

    def add(self, chdir: Path) -> None:
        self.change_dir_to_result(chdir)
        self._formatted_output("add -A .")
        system("git add -A .")

    def clone(self, url: str, result_dir: Path) -> bool:
        self._formatted_output("clone", url)

        try:
            run(["git", "clone", url, str(result_dir)], check=True)
            return True
        except CalledProcessError as e:
            print(f"[fatal] Git clone failed: {e}")
            return False

    def beginning(self, chdir: Path) -> None:
        self.change_dir_to_result(chdir)
        self._formatted_output("clean -fdx")
        self.sh.cmdline("git clean -fdx")

        self._formatted_output("reset --hard origin/$(git rev-parse --abbrev-ref HEAD)")
        self.sh.cmdline("git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)")

        self._formatted_output("fetch --all")
        self.sh.cmdline("git fetch --all")

    def _is_git_repo(self) -> bool:
        result = self.sh.cmdline("git rev-parse --is-inside-work-tree", Popens=True)
        return result == "true"

    def _safe_system(self, cmd: str) -> None:
        if not self._is_git_repo():
            print(
                f"{self.col.RED.value}[warn]{self.col.RESET.value} Not a git repo, skipping: {cmd}"
            )
            return
        system(cmd)

    def commit(self, chdir: Path, message: str = "", noconfirm: bool = False) -> None:
        self.change_dir_to_result(chdir)
        if noconfirm:
            self._formatted_output("commit -m", message)
            self._safe_system(f"git commit -m '{message}'")
        else:
            i = input(
                f"\n {self.col.YELLOW.value}??? {self.col.CYAN.value}{self.col.UNDERLINE_TEXT.value}your message for commit :D ?\n{self.col.YELLOW.value} ~~> : {self.col.RESET.value}"
            )
            self._formatted_output("commit -m", i)
            self._safe_system(f"git commit -m '{i}'")

    def push(self, chdir: Path, branch: str) -> None:
        self.change_dir_to_result(chdir)
        self._formatted_output(f"push origin {branch} --force")
        self._safe_system(f"git push origin {branch} --force")
