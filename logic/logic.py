#!/usr/bin/env python
# --------------------
# ┬  ┌─┐┌─┐┬┌─┐ #-----
# │  │ ││ ┬││   #-----
# ┴─┘└─┘└─┘┴└─┘ #-----
# Copyright (c) 2025 maaru.tan. All Rights Reserved.
# -----------------------------------------------------

# -----[ Variables ]

DEBUG = False

# ---------------------

import json
from pathlib import Path
from shutil import copytree, rmtree
from shutil import copy, copy2
from time import sleep, localtime
from subprocess import PIPE, run, Popen, CalledProcessError
from typing import Optional
from os import listdir, chdir
from os import system as shell
from sys import exit
from argparse import ArgumentParser

# ----- [ Paths ]
HOME = Path.home()
HEREDIR = Path(__file__).parent.parent
DIST = HEREDIR / "dist"
BASEJSON = HEREDIR / "base.json"
LOGGFILE = HEREDIR / ".current.log"


# ---------------------------------------------


def main():
    arguments()


# ---------------------------------------------


class Styles:
    HEADER = "\033[95m"
    YELLOW = "\033[93m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    OKPURPLE = "\033[35m"
    WARN = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    def __init__(self, col: str = ENDC, content: str = "Enter content") -> None:
        self.font = self._fonts().get("calvin_s")
        self.col = col
        if not self.font:
            raise ValueError(f"Font 'calvin_s' not found.")
        self.content = content

    def _fonts(self) -> dict:
        return {
            "calvin_s": {
                "a": "┌─┐\n├─┤\n┴ ┴",
                "b": "┌┐ \n├┴┐\n└─┘",
                "c": "┌─┐\n│  \n└─┘",
                "d": "┌┬┐\n ││\n─┴┘",
                "e": "┌─┐\n├─ \n└─┘",
                "f": "┌─┐\n├┤ \n└",
                "g": "┌─┐\n│ ┬\n└─┘",
                "h": "┬ ┬\n├─┤\n┴ ┴",
                "i": "┬\n│\n┴",
                "j": " ┬\n │\n└┘",
                "k": "┬┌─\n├┴┐\n┴ ┴",
                "l": "┬  \n│  \n┴─┘",
                "m": "┌┬┐\n│││\n┴ ┴",
                "n": "┌┐┌\n│││\n┘└┘",
                "o": "┌─┐\n│ │\n└─┘",
                "p": "┌─┐\n├─┘\n┴  ",
                "q": "┌─┐ \n│─┼┐\n└─┘└",
                "r": "┬─┐\n├┬┘\n┴└─",
                "s": "┌─┐\n└─┐\n└─┘",
                "t": "┌┬┐\n │ \n ┴ ",
                "u": "┬ ┬\n│ │\n└─┘",
                "v": "┬  ┬\n└┐┌┘\n └┘",
                "w": "┬ ┬\n│││\n└┴┘",
                "x": "─┐ ┬\n┌┴┬┘\n┴ └─",
                "y": "┬ ┬\n└┬┘\n ┴ ",
                "z": "┌─┐\n┌─┘\n└─┘",
            },
        }

    def render(self):
        lines = [""] * 3
        for char in self.content:
            char_lines = self.font.get(char.lower(), "   \n   \n   ").split("\n")  # type: ignore
            for i in range(3):
                lines[i] += char_lines[i] + ""
        return "\n".join(lines)

    def __str__(self) -> str:
        try:
            return f"{self.col}" + self.render() + f"{self.ENDC}"
        except Exception:
            return "Error: no valid font"


def does_path_exists(path) -> bool:
    return bool(Path(path).exists())


class FileManager:
    def __init__(
        self,
        path: Path = Path(""),
        content: str = "",
    ) -> None:
        """Constructor for FileManager class."""
        self.path = path
        self.content = content

    def write(self) -> None:
        "Writes a file specified by path"
        try:
            with open(self.path, "w") as f:
                f.write(self.content)
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"write_file failed: {e}")

    def append(self) -> None:
        "Appends a file specified by path"
        try:
            with open(self.path, "a") as f:
                f.write(self.content)
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"append_file failed: {e}")

    def read(self) -> str:
        try:
            with open(self.path, "r") as f:
                return f.read()
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"read_file failed: {e}")
            return ""

    def delete_file(self) -> None:
        "Deletes a file specified by path"
        try:
            if self.path.is_file():
                self.path.unlink()
            else:
                Logger(
                    path=LOGGFILE,
                    status="i",
                    content=f"Path is not a file: {self.path}",
                )
            #     self.delete_dir()

        except Exception as e:
            Logger(
                path=LOGGFILE,
                status="i",
                content=f"delete_file failed for {self.path}: {e}",
            )

    def delete_dir(self) -> None:
        "Deletes a directory specified by path"
        try:
            if self.path.is_dir():
                rmtree(self.path)
            else:
                Logger(
                    path=LOGGFILE,
                    status="e",
                    content=f"Path is not a directory: {self.path}",
                )

        except Exception as e:
            Logger(
                path=LOGGFILE,
                status="e",
                content=f"delete_dir failed for {self.path}: {e}",
            )

    def __str__(self) -> str:
        "Returns a string representation of the class"
        return (
            f"FileManager(path={self.path}, content={self.content})\n"
            "Please use: write, append, read, delete_file, delete_dir\n"
            "For example: f = FileManager(path, content)\n"
            "f.write(), f.append(), f.read(), f.delete_file(), f.delete_dir()"
        )


class Logger:
    def __init__(
        self,
        path: Path = Path(""),
        status: str = "info",
        content: str = "",
    ) -> None:
        """Constructor for Logger class"""

        self.path = path
        self.status = status.lower()
        self.content = content
        self.state = {
            "info": "i",
            "warn": "w",
            "error": "e",
            "debug": "d",
        }

        self.F = FileManager(path=self.path)
        try:
            self.handle_log()
        except Exception as e:
            print(f"class Logger failed: {e}")

    def current_time(self) -> str:
        """Returns the current time"""

        now = localtime()
        return f"{now.tm_mday:02d}.{now.tm_mon:02d}.{now.tm_year} {now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}"

    def write(self, content: str = "") -> None:
        """Palimorphism from the inheriting class FileManager method write"""
        try:
            self.F.content = content if content else self.content
            self.F.append()
        except Exception as e:
            print(f"class Logger failed: {e}")

    def handle_log(self):
        """Handles the log based on the status"""
        cmd = self.status

        def render_handle_log() -> None:
            logo = ""
            for k, v in self.state.items():
                if cmd == v or cmd == k:
                    logo = k.upper()

            crt = self.current_time()

            if ":" in self.content:
                msg, path = self.content.split(":", 1)
                msg = msg.strip() + ":"
                path = path.strip()
            else:
                msg = self.content
                path = ""

            logo_width = 6
            msg_width = 28
            path_width = 55

            logo_str = f"{logo:<{logo_width}}"
            msg_str = f"{msg:<{msg_width}}"
            path_str = f"{path:<{path_width}}"

            content = f"{logo_str}| {msg_str}| {path_str}| {crt}\n"
            self.write(content)

        if cmd != "":
            render_handle_log()
        else:
            print("class Logger failed: status is empty")

    def __str__(self) -> str:
        """Returns a string representation of the class"""
        return (
            f"class Logger:\nLogger write content in the file specified path\n"
            f"Please use: \n"
            f"  l = Logger\n"
            f"  l(path, status, content)\n"
            f"---------------------------\n"
            f"content write to that:\n"
            f"  INFO: [ content ] {self.current_time()}\n"
        )


def cmdline(
    command: str = "echo enter your command :D",
    Popens: bool = False,
    runs: bool = True,
) -> Optional[str]:
    try:
        if Popens:
            process = Popen(
                command,
                shell=True,
                text=True,
                stdout=PIPE,
                stderr=PIPE,
            )
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                return f"Error: {stderr.strip()}"
        elif runs:
            result = run(
                command,
                shell=True,
                text=True,
                stdout=PIPE,
                stderr=PIPE,
                check=True,
            )
            stdout = result.stdout
        else:
            Logger(path=LOGGFILE, status="e", content="cmdline invalid arguments :(")
            return "Error: cmdline invalid arguments :("

        return f"{stdout.strip()}"

    except CalledProcessError as e:
        Logger(path=LOGGFILE, status="e", content=f"cmdline: {e.stderr}")
    except Exception as e:
        Logger(path=LOGGFILE, status="e", content=f"cmdline: {e}")


class JsonManager:
    def __init__(self, path: Path = Path("")) -> None:
        """Constructor for baseJson class."""
        f = FileManager
        self.path = path
        try:
            if not does_path_exists(self.path):
                f(self.path, "{}").write()
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"init_json failed: {e}")

    def read(self) -> dict:
        """Reads a json specified by path."""
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"read_json failed: {e}")
            return {}

    def write(self, data) -> None:
        """Writes a json specified by path."""
        try:
            with open(self.path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"write_json failed: {e}")

    def get_data(self) -> dict:
        """Reads a json specified by path."""
        if does_path_exists(self.path):
            try:
                data = self.read()
            except Exception as e:
                Logger(path=LOGGFILE, status="e", content=f"read_json failed: {e}")
                data = {}
        else:
            data = {}
        return data

    def append(self, item) -> None:
        """Appends an item to a json specified by path."""
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise TypeError("JSON root is not a list — can't append item.")
            data.append(item)
            self.write(data)
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"append failed: {e}")


class Git:
    def __init__(self) -> None:
        self.col = Styles

    def add(self) -> None:
        col = self.col
        try:
            print(
                f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}add -A .{col.ENDC}"
            )
            shell("git add -A .")
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"git add failed: {e}")

    def clone(self, url: str) -> None:
        col = self.col
        try:
            print(
                f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN}  {col.UNDERLINE}clone {url}{col.ENDC}"
            )
            shell(f"git clone {url}")
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"git clone failed: {e}")

    def beginning(self) -> None:
        try:
            col = self.col
            print(
                f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}clean -fdx{col.ENDC}"
            )
            cmdline("git clean -fdx")
            print(
                f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}reset --hard origin/$(git rev-parse --abbrev-ref HEAD){col.ENDC}"
            )
            cmdline("git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)")
            print(
                f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}fetch --all{col.ENDC}"
            )
            cmdline("git fetch --all")
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"git beginning failed: {e}")

    def commit(
        self,
        massage: str = "",
        noconfirm: bool = False,
    ) -> None:
        col = self.col
        try:
            if noconfirm:
                print(
                    f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}commit -m '{massage}'{col.ENDC}"
                )
                print()
                shell(f"git commit -m '{massage}'")
            else:
                i = input(
                    f"{col.YELLOW}!!! {col.OKCYAN}{col.UNDERLINE}your message for commit :D ?\n{col.YELLOW} ~~> : {col.ENDC}"
                )
                print(
                    f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}commit -m '{i}'{col.ENDC}"
                )
                shell(f"git commit -m '{i}'")
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"git commit failed: {e}")

    def push(self) -> None:
        col = self.col
        try:
            print(
                f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}push origin HEAD{col.ENDC}"
            )
            print()
            shell(f"git push origin HEAD")
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"git push failed: {e}")


class BaseJsonHandler:
    def __init__(
        self,
        dirname: str,
        url: str,
        branch: str,
        noconfirm: bool,
        inside: bool,
        gitignore: list,
        blacklist: list,
    ) -> None:
        self.dirname = dirname
        self.url = url
        self.branch = branch
        self.gitignore = gitignore
        self.blacklist = blacklist
        self.noconfirm = noconfirm
        self.inside = inside

        try:
            self.base_push_handler()
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"base_push_handler failed: {e}")
        try:
            self.more_push_handler()
        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"more_push_handler failed: {e}")

    def base_push(
        self,
        *extra_entries: dict,
        push_object: dict,
    ) -> None:
        j = JsonManager(BASEJSON)
        try:
            data = j.get_data() if does_path_exists(BASEJSON) else {}
            data[self.dirname] = {
                "dirname": self.dirname,
                "url": self.url,
                "branch": self.branch,
                "push_object": push_object,
            }

            if "push_more" in data and not data["push_more"]:
                del data["push_more"]

            j.write(data)

            for entry in extra_entries:
                try:
                    j.append(entry)
                except Exception as e:
                    Logger(path=LOGGFILE, status="e", content=f"append failed: {e}")

        except Exception as e:
            Logger(path=LOGGFILE, status="e", content=f"dump_json failed: {e}")

    def push_more(
        self,
        *repos: dict,
    ) -> None:
        j = JsonManager(BASEJSON)
        data = j.get_data() if does_path_exists(BASEJSON) else {}

        if not repos:
            return

        data["push_more"] = {}

        for i, repo in enumerate(repos, start=1):
            if isinstance(repo, dict) and all(
                k in repo for k in ["dirname", "url", "branch"]
            ):
                data["push_more"][str(i)] = repo
            else:
                Logger(
                    path=LOGGFILE,
                    status="e",
                    content=f"Invalid format for repo #{i}: {repo}",
                )

        j.write(data)

    def push_logic(
        self,
        dirname: str,
        inside: bool,
        branch: str,
        url: str,
        push_object: dict,
        blacklist: list,
        gitignore: list,
        noconfirm: bool,
    ) -> None:
        g = Git()
        f = FileManager
        dict_keys = []
        dirs = []
        files = []
        path_dir = DIST / dirname
        Path(path_dir).mkdir(exist_ok=True, parents=True)
        listD = listdir(path_dir)

        if push_object == {}:
            Logger(path=LOGGFILE, status="e", content="push_object is empty")
            return

        def rm_all_without_git(ExistDotgit: bool = True) -> None:
            chdir(path_dir)
            if not ExistDotgit:
                g.beginning()
            for i in listD:
                if i != ".git":
                    f(path_dir / i).delete_file()
                    f(path_dir / i).delete_dir()
                else:
                    Logger(
                        path=LOGGFILE,
                        status="e",
                        content="push_logic: can't remove objects where `.git`",
                    )

        def copy_base_push_json_paths() -> None:
            for key, value in push_object.items():
                if isinstance(value, dict):
                    data = key, value
                    dict_keys.append(data)
                elif isinstance(value, str):
                    p = Path(value)
                    if p.is_dir():
                        dirs.append(key)
                    elif p.is_file():
                        files.append(key)
                    else:
                        Logger(
                            path=LOGGFILE,
                            status="e",
                            content=f"Unsupported type: {value}",
                        )
                else:
                    Logger(
                        path=LOGGFILE,
                        status="e",
                        content=f"Unknown type for '{key}': {type(value)}",
                    )

            def CopyTreeSafe(src: Path, dst: Path) -> None:
                src = src.resolve()
                dst = dst.resolve()

                if dst == src or dst.is_relative_to(src):
                    Logger(
                        path=LOGGFILE,
                        status="e",
                        content=f"Skipping: trying to copy {src} into its subdir {dst}",
                    )
                    return

                def ignore_git_dirs(dir, contents):
                    return [entry for entry in contents if entry in blacklist]

                try:
                    if src.is_file():
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        copy2(src, dst)
                    elif src.is_dir():
                        copytree(src, dst, dirs_exist_ok=True, ignore=ignore_git_dirs)
                    else:
                        Logger(
                            path=LOGGFILE,
                            status="e",
                            content=f"Unsupported source type: {src}",
                        )
                except Exception as e:
                    Logger(
                        path=LOGGFILE,
                        status="w",
                        content=f"Failed to copy {src} → {dst}: {e}",
                    )

            def walk_push_object(obj, prefix=Path(), inside=inside):
                if isinstance(obj, str):
                    src = Path(obj)
                    if inside and src.is_dir():
                        for child in src.iterdir():
                            yield (child.name, child)
                    else:
                        yield (prefix, src)
                elif isinstance(obj, dict):
                    for key, value in obj.items():
                        if inside and isinstance(value, str) and Path(value).is_dir():
                            yield from walk_push_object(value, Path(), inside=True)
                        else:
                            yield from walk_push_object(value, prefix / key, inside)
                else:
                    raise ValueError(f"Unsupported value in push_object: {obj!r}")

            for relative_dst, src in walk_push_object(push_object, inside=inside):
                dst = path_dir / relative_dst
                if does_path_exists(src):
                    if dst.exists() and inside:
                        if dst.is_dir():
                            rmtree(dst)
                        else:
                            dst.unlink()
                    CopyTreeSafe(src, dst)
                else:
                    Logger(
                        path=LOGGFILE, status="e", content=f"Source not found: {src}"
                    )

            for d in dirs:
                path = path_dir / d
                CopyTreeSafe(HOME / d, path)

            for f in files:
                path = path_dir / f
                copy(HOME / f, path)

            f = FileManager
            git_ignore_path = path_dir / ".gitignore"
            content = "\n".join(gitignore)
            f(git_ignore_path, content).write()

        art_git_clone = Styles(col=Styles.OKGREEN, content="git clone")
        art_git_exists = Styles(col=Styles.OKGREEN, content="git exists")

        line = "▁" * 50 + "\n"
        col = Styles

        if does_path_exists(path_dir / ".git"):
            print(art_git_exists)
            print(line)
            rm_all_without_git(ExistDotgit=False)
            copy_base_push_json_paths()
            g.add()
            g.commit(massage="no massage | script push", noconfirm=noconfirm)
            print()
            g.push()
            print()
            print(line)
        else:
            print(line)
            f(path_dir).delete_dir()

            print(art_git_clone)
            g.clone(f"{url} {path_dir}")
            rm_all_without_git()
            copy_base_push_json_paths()
            g.add()
            g.commit(massage="no massage | script push", noconfirm=noconfirm)
            print()
            g.push()
            print()
            print(line)

    def more_push_handler(self) -> None:
        j = JsonManager(BASEJSON)
        data = j.get_data()
        pm_data = data["push_more"]

        pm_data_id = []
        for k, v in pm_data.items():
            pm_data_id.append(k)

        for i in pm_data_id:
            dirname = f"{pm_data[i]['dirname']}"
            url = f"{pm_data[i]['url']}"
            branch = f"{pm_data[i]['branch']}"
            push_object = dict(pm_data[i]["push_object"])
            inside = pm_data[i]["inside"]
            self.push_logic(
                dirname=dirname,
                url=url,
                branch=branch,
                inside=inside,
                push_object=push_object,
                noconfirm=self.noconfirm,
                gitignore=self.gitignore,
                blacklist=self.blacklist,
            )

    def base_push_handler(self) -> None:
        j = JsonManager(BASEJSON)
        data = j.get_data()
        self.push_logic(
            dirname=self.dirname,
            url=self.url,
            branch=self.branch,
            push_object=data[self.dirname]["push_object"],
            noconfirm=self.noconfirm,
            gitignore=self.gitignore,
            blacklist=self.blacklist,
            inside=self.inside,
        )


def arguments() -> None:
    parser = ArgumentParser(description="push dotfiles :D")
    parser.add_argument("-l", "--list", action="store_true", help="list dotfiles")
    args = parser.parse_args()

    if args.list:
        print("list dotfiles")
