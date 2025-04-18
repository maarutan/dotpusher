#!/usr/bin/env python
# -------------------
# ┌─┐┬ ┬┌─┐┬ ┬ #-----
# ├─┘│ │└─┐├─┤ #-----
# ┴  └─┘└─┘┴ ┴ #-----
# Copyright (c) 2025 maaru.tan. All Rights Reserved.
# -------------------------------
from logic.logic import *  # ----

# -------------------------------
j = BaseJsonHandler(
    dirname="dotfiles",
    url="git@github.com:maarutan/dotfiles.git",
    branch="master",
    # -------------
    gitignore=[
        ".git/",
        "**/.git/",
        ".git/**",
    ],
    blacklist=[
        ".git",
        "__pycache__",
    ],
)

j.base_push(
    # ------------------------------------------
    push_object={
        ".config": {
            "yazi": f"{HOME}/.config/yazi",
        },
        ".local": {"bin": f"{HOME}/.local/bin"},
        ".themes": f"{HOME}/.themes",
    },
)

j.push_more(
    {
        "dirname": "",
        "url": "",
        "branch": "",
        # ------------------------------------------
        "push_object": {},
    },
)
