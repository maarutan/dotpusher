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

import subprocess
import json
import time
import typing
import pathlib
import sys
import shutil
import argparse
import os

# ---------------------
Sleep = time.sleep
Run = subprocess.run
Popen = subprocess.Popen
Optional = typing.Optional
Path = pathlib.Path
Exit = sys.exit
ArgPars = argparse.ArgumentParser
Chdir = os.chdir
ListDir = os.listdir
CopyTree = shutil.copytree
CopyFile = shutil.copy
Shell = os.system
# ---------------------

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


class Colors:
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


def RmFile(path: Path) -> None:
    try:
        if path.is_file():
            path.unlink()
    except Exception as e:
        logger("error", f"RmFile failed for {path}: {e}")


def RmDir(path: Path) -> None:
    try:
        if path.is_dir():
            shutil.rmtree(path)
    except Exception as e:
        logger("error", f"RmDir failed for {path}: {e}")


def path_exists(path) -> bool:
    return bool(Path(path).exists())


def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)


def append_file(path, content):
    with open(path, "a") as f:
        f.write(content)


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def logger(
    lvl: str = "info",
    *args: str,
) -> None:
    # - var
    col = Colors
    lvl = lvl.lower()
    nerd = check_nerd_font()

    # - func
    def current_time() -> str:
        now = time.localtime()
        return f"{now.tm_mday:02d}.{now.tm_mon:02d}.{now.tm_year} {now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}"

    def lvl_icon(pretty: bool = False) -> str:
        match lvl:
            case "error":
                return (
                    f"{col.FAIL}ERR 󰅚 {col.ENDC}"
                    if nerd and pretty
                    else f"{col.FAIL}Error{col.ENDC}"
                    if pretty
                    else "ERR 󰅚"
                    if nerd
                    else "Error"
                )
            case "warn":
                return (
                    f"{col.WARN}WARN 󰀪 {col.ENDC}"
                    if nerd and pretty
                    else f"{col.WARN}Warn{col.ENDC}"
                    if pretty
                    else "WARN 󰀪"
                    if nerd
                    else "Warn"
                )
            case "info":
                return (
                    f"{col.OKBLUE}INFO  {col.ENDC}"
                    if nerd and pretty
                    else f"{col.OKBLUE}Info{col.ENDC}"
                    if pretty
                    else "INFO "
                    if nerd
                    else "Info"
                )
            case _:
                return "Log"

    # - build
    pretty_lvl = lvl_icon(pretty=True)
    log_lvl = lvl_icon(pretty=False)
    message = f"{log_lvl} : [ {' '.join(args)} ] {current_time()}\n"
    message_pretty = f"{pretty_lvl} : [ {' '.join(args)} ] {current_time()}\n"

    # - print
    if DEBUG:
        print(message_pretty)

    # - write
    if not path_exists(LOGGFILE):
        write_file(LOGGFILE, message)
    else:
        append_file(LOGGFILE, message)


def cmdline(
    command: str = "echo enter your command :D",
    Popens: bool = False,
    Runs: bool = True,
) -> Optional[str]:
    try:
        if Popens:
            process = subprocess.Popen(
                command,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                return f"Error: {stderr.strip()}"
        elif Runs:
            result = subprocess.run(
                command,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            stdout = result.stdout
        else:
            logger("error", "invalid arguments :(")
            return "Error: invalid arguments :("

        return f"{stdout.strip()}"

    except subprocess.CalledProcessError as e:
        logger("error", f"{e.stderr}")
    except Exception as e:
        logger("error", f"{e}")


def check_nerd_font() -> str | bool:
    font = bool(cmdline("fc-list | grep Nerd"))
    return font if font else "Error: Nerd Font not found"


class baseJson:
    def __init__(self) -> None:
        if not path_exists(BASEJSON):
            write_file(BASEJSON, "{}")

    def read(self) -> dict:
        try:
            with open(BASEJSON, "r") as f:
                return json.load(f)
        except Exception as e:
            logger("error", f"read_json failed: {e}")
            return {}

    def write(self, data) -> None:
        try:
            with open(BASEJSON, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger("error", f"write_json failed: {e}")

    def get_data(self) -> dict:
        if path_exists(BASEJSON):
            try:
                data = self.read()
            except Exception as e:
                logger("error", f"read_json failed: {e}")
                data = {}
        else:
            data = {}
        return data

    def append(self, item) -> None:
        try:
            with open(BASEJSON, "r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise TypeError("JSON root is not a list — can't append item.")

            data.append(item)
            with open(BASEJSON, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger("error", f"append failed: {e}")


class Git:
    def __init__(self) -> None:
        self.col = Colors()

    def add(self) -> None:
        col = self.col
        try:
            print(
                f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}add -A .{col.ENDC}"
            )
            Shell("git add -A .")
        except Exception as e:
            logger("error", f"git add failed: {e}")

    def clone(self, url: str) -> None:
        col = self.col
        try:
            print(
                f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN}  {col.UNDERLINE}clone {url}{col.ENDC}"
            )
            Shell(f"git clone {url}")
        except Exception as e:
            logger("error", f"git clone failed: {e}")

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
            logger("error", f"git beginning failed: {e}")

    def commit(
        self,
        name: str = "",
        noconfirm: bool = False,
    ) -> None:
        col = self.col
        try:
            if noconfirm:
                print(
                    f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}commit -m '{name}'{col.ENDC}"
                )
                print()
                Shell(f"git commit -m '{name}'")
            else:
                i = input(
                    f"{col.YELLOW}!!! {col.OKCYAN}{col.UNDERLINE}your message for commit :D ?\n{col.YELLOW} ~~> : {col.ENDC}"
                )
                print(
                    f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}commit -m '{i}'{col.ENDC}"
                )
                Shell(f"git commit -m '{i}'")
        except Exception as e:
            logger("error", f"git commit failed: {e}")

    def push(self) -> None:
        col = self.col
        try:
            print(
                f"{col.YELLOW}~~>  {col.OKPURPLE}git{col.OKCYAN} {col.UNDERLINE}push origin HEAD{col.ENDC}"
            )
            print()
            Shell(f"git push origin HEAD")
        except Exception as e:
            logger("error", f"git push failed: {e}")


class BaseJsonHandler:
    def __init__(
        self,
        dirname: str,
        url: str,
        branch: str,
        gitignore: list,
        blacklist: list,
    ) -> None:
        self.dirname = dirname
        self.url = url
        self.branch = branch
        self.gitignore = gitignore
        self.blacklist = blacklist
        self.base_push_handler()

    def base_push(
        self,
        *extra_entries: dict,
        push_object: dict,
    ) -> None:
        j = baseJson()
        try:
            data = j.get_data() if path_exists(BASEJSON) else {}
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
                    logger("error", f"append failed: {e}")

        except Exception as e:
            logger("error", f"dump_json failed: {e}")

    def push_more(self, *repos) -> None:
        j = baseJson()
        data = j.get_data() if path_exists(BASEJSON) else {}

        if not repos:
            return

        data["push_more"] = {}

        for i, repo in enumerate(repos, start=1):
            if isinstance(repo, dict) and all(
                k in repo for k in ["dirname", "url", "branch"]
            ):
                data["push_more"][str(i)] = repo
            else:
                logger("error", f"Invalid format for repo #{i}: {repo}")

        j.write(data)

    def base_push_handler(self) -> None:
        g = Git()
        path_dir = HEREDIR / "dist" / self.dirname
        Path(path_dir).mkdir(exist_ok=True, parents=True)
        listD = ListDir(path_dir)
        j = baseJson()
        data = j.get_data()
        dir_object = data[self.dirname]["push_object"]

        dict_keys = []
        dirs = []
        files = []

        def rm_all_without_git(ExistDotgit: bool = True) -> None:
            Chdir(path_dir)
            if not ExistDotgit:
                g.beginning()
            for i in listD:
                if i != ".git":
                    RmDir(path_dir / i)
                    RmFile(path_dir / i)
                else:
                    logger("error", f"can't remove objects where .git")

        def copy_base_push_json_paths() -> None | list:
            for key, value in dir_object.items():
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
                        logger(
                            "error",
                            f"Unknown or non-existent path for '{key}': {value}",
                        )
                else:
                    logger("error", f"Unknown type for '{key}': {type(value)}")

            def CopyTreeSafe(src: Path, dst: Path) -> None:
                src = src.resolve()
                dst = dst.resolve()

                if dst == src or dst.is_relative_to(src):
                    logger(
                        "error", f"Skipping: trying to copy {src} into its subdir {dst}"
                    )
                    return

                def ignore_git_dirs(dir, contents):
                    ignored = []
                    for entry in contents:
                        if entry in self.blacklist:
                            ignored.append(entry)
                    return ignored

                try:
                    shutil.copytree(
                        src, dst, dirs_exist_ok=True, ignore=ignore_git_dirs
                    )
                except Exception as e:
                    logger("error", f"Failed to copy {src} → {dst}: {e}")

            for parent_dir, children in dict_keys:
                for child_name, full_path in children.items():
                    src = Path(full_path)
                    dst = path_dir / parent_dir / child_name
                    CopyTreeSafe(src, dst)

            for d in dirs:
                path = path_dir / d
                CopyTreeSafe(HOME / d, path)

            for f in files:
                path = path_dir / f
                CopyFile(HOME / f, path)

            git_ignore_path = path_dir / ".gitignore"
            content = "\n".join(self.gitignore)
            write_file(git_ignore_path, content)

        art_git_exists = """
            ┌─┐┬┌┬┐  ┌─┐─┐ ┬┬┌─┐┌┬┐
            │ ┬│ │   ├┤ ┌┴┬┘│└─┐ │ 
           o└─┘┴ ┴   └─┘┴ └─┴└─┘ ┴ 
        """

        if path_exists(path_dir / ".git"):
            col = Colors()
            print(f"{col.OKGREEN}{art_git_exists}{col.ENDC}")
            print("▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n")
            rm_all_without_git(ExistDotgit=False)
            copy_base_push_json_paths()
            g.add()
            g.commit(name="no massage | script push", noconfirm=True)
            print()
            g.push()
            print()
            print("▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n")
        else:
            art_git_clone = """
                ┌─┐┬┌┬┐  ┌─┐┬  ┌─┐┌┐┌┌─┐
                │ ┬│ │   │  │  │ ││││├┤ 
                └─┘┴ ┴   └─┘┴─┘└─┘┘└┘└─┘
            """
            print("▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n")
            # if not path_exists(path_dir) and not path_exists(path_dir / ".git"):
            RmDir(path_dir)
            g.clone(f"{self.url} {path_dir}")
            rm_all_without_git()
            copy_base_push_json_paths()
            g.add()
            g.commit(name="no massage | script push", noconfirm=True)
            print()
            g.push()
            print()
            print("▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n")


def arguments() -> None:
    parser = ArgPars(description="push dotfiles :D")
    parser.add_argument("-l", "--list", action="store_true", help="list dotfiles")
    args = parser.parse_args()

    if args.list:
        print("list dotfiles")
