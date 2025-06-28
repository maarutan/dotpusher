from filecmp import cmp, dircmp
from .cli import Cli
from pathlib import Path
from time import sleep
from os import chdir, listdir
from shutil import copy2, copytree
from pathlib import Path

from modules import JsonManager, FileManager, Git, Col, Shell


class PrepareDir:
    def __init__(self) -> None:
        self.g = Git()
        self.p = Path
        self.jm = JsonManager
        self.fm = FileManager
        self.cli = Cli()
        self.col = Col
        self.sh = Shell()
        self.confh = self.cli.get_config_handler()
        self.result_dir = self.confh.get_result_dir()

    def is_git(self) -> bool:
        if (
            self.fm(self.result_dir).is_exists()
            and self.fm(self.result_dir / ".git").is_exists()
        ):
            return True
        return False

    def change_dir_to_result(self) -> None:
        if not self.result_dir.exists():
            raise RuntimeError(f"Result dir does not exist: {self.result_dir}")
        chdir(self.result_dir)

    def rm_all_without_git(self, ExistDotgit: bool = True) -> None:
        if not ExistDotgit:
            self.g.beginning(self.result_dir)

        for i in listdir(self.result_dir):
            if i != ".git":
                self.fm(self.result_dir / i).delete()
            else:
                print(
                    "prepare_dir (rm_all_without_git): can't remove objects where `.git`"
                )

    def path_handler(
        self,
        path: Path,
        if_path_only_name: str = "",
        without_tilde: bool = False,
    ) -> Path:
        path_str = str(path).strip()

        if without_tilde:
            if path_str.startswith("~"):
                no_tilde = path_str.replace("~", "", 1).lstrip("/")
                return self.p(no_tilde)
            elif path_str.startswith("/"):
                no_slash = path_str.lstrip("/")
                return self.p(no_slash)
            elif not path_str.startswith("/") and "/" not in path_str:
                return self.p(if_path_only_name) / path_str
            return self.p(path_str)
        else:
            if (
                not path_str.startswith("~")
                and not path_str.startswith("/")
                and if_path_only_name
            ):
                return self.p(if_path_only_name).expanduser() / path_str
            return self.p(path_str).expanduser()

    def _copy_and_overwrite_safe(self, src: Path, dst: Path) -> None:
        src = src.resolve()
        dst = dst.resolve()

        final_dst = dst / src.name

        if final_dst == src or final_dst.is_relative_to(src):
            print(f"Skipping: trying to copy {src} into its subdir {final_dst}")
            return

        def ignore_list_from_blacklist(dir, contents):
            return [entry for entry in contents if entry in self.confh.get_blacklist()]

        try:
            if src.is_file():
                final_dst.parent.mkdir(parents=True, exist_ok=True)
                if final_dst.exists():
                    final_dst.unlink()
                copy2(src, final_dst)

            elif src.is_dir():
                if final_dst.exists() and final_dst.is_dir():
                    self.fm(final_dst).delete()

                copytree(src, final_dst, ignore=ignore_list_from_blacklist)

            else:
                print(f"Unsupported source type: {src}")

        except Exception as e:
            print(f"Failed to copy {src} → {final_dst}: {e}")

    def _copy_tree_safe(self, src: Path, dst: Path) -> None:
        src = src.resolve()
        dst = dst.resolve()

        final_dst = dst / src.name

        if final_dst == src or final_dst.is_relative_to(src):
            print(f"Skipping: trying to copy {src} into its subdir {final_dst}")
            return

        def ignore_git_dirs(dir, contents):
            return [entry for entry in contents if entry in self.confh.get_blacklist()]

        try:
            if src.is_file():
                final_dst.parent.mkdir(parents=True, exist_ok=True)
                copy2(src, final_dst)
            elif src.is_dir():
                copytree(src, final_dst, dirs_exist_ok=True, ignore=ignore_git_dirs)
            else:
                print(f"Unsupported source type: {src}")
        except Exception as e:
            print(f"Failed to copy {src} → {final_dst}: {e}")

    def arrow_title(self, title: str, line: int = 50, pad: int = 1) -> None:
        print(
            " " * pad
            + f"{self.col.YELLOW.value}"
            + "-" * line
            + f" {self.col.RESET.value}==\\"
        )

        clean_title = title.upper()
        centered_title = clean_title.center(line)

        start = centered_title.find(clean_title)
        end = start + len(clean_title)

        colored_line = (
            centered_title[:start]
            + f"{self.col.GREEN.value}{self.col.BOLD.value}{self.col.UNDERLINE_TEXT.value}"
            + clean_title
            + f"{self.col.RESET.value}"
            + centered_title[end:]
        )

        print(" " * pad + f"{colored_line} ======>")

        print(
            " " * pad
            + f"{self.col.YELLOW.value}"
            + "-" * line
            + f" {self.col.RESET.value}==/"
        )

    def should_replace_file(self, src: Path, dst: Path) -> bool:
        return not dst.exists() or not dst.is_file() or not cmp(src, dst, shallow=False)

    def is_dir_empty(self, path: Path) -> bool:
        return path.is_dir() and not any(path.iterdir())

    def should_replace_dir(self, src: Path, dst: Path) -> bool:
        if not dst.exists():
            return True
        if not src.is_dir() or not dst.is_dir():
            return True
        if self.is_dir_empty(src) and self.is_dir_empty(dst):
            return False

        comparison = dircmp(src, dst)
        if comparison.left_only or comparison.right_only or comparison.diff_files:
            return True

        for sub in comparison.common_dirs:
            if self.should_replace_dir(src / sub, dst / sub):
                return True

        return False

    def assets_handler(self, assets_dir: Path) -> None:
        if not assets_dir.exists():
            assets_dir.mkdir(parents=True, exist_ok=True)

        empty_items = []
        for i in assets_dir.iterdir():
            empty_items.append(i)

        for j in empty_items:
            self._copy_tree_safe(j, self.result_dir)

    def walk_and_copy_on_dir(self, title: str, replace: bool = False) -> None:
        self.arrow_title(title)

        self.assets_handler(self.confh.get_assets())

        for k, v in self.confh.get_resources().items():
            expanded_key = self.p(k).expanduser()
            base_dir = (
                self.result_dir
                if str(k).strip() in ("~", "~/")
                else self.result_dir / expanded_key.name
            )
            base_dir.mkdir(parents=True, exist_ok=True)

            for item in v:
                item_path = self.path_handler(
                    self.p(item),
                    without_tilde=False,
                    if_path_only_name=k,
                )

                if not item_path.exists():
                    print(
                        f"{self.col.YELLOW.value}[warn]   "
                        f"{self.col.RED.value}missing : "
                        f"{self.col.PURPLE.value}{self.col.UNDERLINE_TEXT.value}{str(item_path):<45}"
                        f"{self.col.RESET.value} {self.col.BOLD.value}→{self.col.RESET.value} "
                        f"{self.col.PURPLE.value}(path does not exist){self.col.RESET.value}"
                    )
                    sleep(float(self.confh.get_warn_timeout()))
                    continue

                expanded_item_path = self.p(item).expanduser()

                if expanded_item_path.is_absolute():
                    target_path = base_dir / expanded_item_path.name
                elif "/" in item:
                    target_path = base_dir / item
                else:
                    target_path = base_dir / item

                target_path.parent.mkdir(parents=True, exist_ok=True)

                if replace:
                    should_replace = False

                    if item_path.is_file():
                        should_replace = self.should_replace_file(
                            item_path, target_path
                        )
                    elif item_path.is_dir():
                        should_replace = self.should_replace_dir(item_path, target_path)

                    if should_replace:
                        print(
                            f"{self.col.CYAN.value}[info]   "
                            f"{self.col.BLUE.value}replace : "
                            f"{self.col.PURPLE.value}{self.col.UNDERLINE_TEXT.value}{str(item_path):<45}"
                            f"{self.col.RESET.value} {self.col.BOLD.value}→{self.col.RESET.value} "
                            f"{self.col.PURPLE.value}{self.col.UNDERLINE_TEXT.value}{str(target_path):<45}"
                            f"{self.col.RESET.value}"
                        )
                        self._copy_and_overwrite_safe(item_path, target_path.parent)
                    else:
                        print(
                            f"{self.col.GREEN.value}[skip same]{self.col.RESET.value} {item_path}"
                        )
                else:
                    print(
                        f"{self.col.CYAN.value}[info]   "
                        f"{self.col.BLUE.value}copy : "
                        f"{self.col.PURPLE.value}{self.col.UNDERLINE_TEXT.value}{str(item_path):<45}"
                        f"{self.col.RESET.value} {self.col.BOLD.value}→{self.col.RESET.value} "
                        f"{self.col.PURPLE.value}{self.col.UNDERLINE_TEXT.value}{str(target_path):<45}"
                        f"{self.col.RESET.value}"
                    )
                    self._copy_tree_safe(item_path, target_path.parent)

                sleep(0.08)
