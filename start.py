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
            "kitty": f"{HOME}/.config/kitty",
            "zsh": f"{HOME}/.config/zsh",
            "btop": f"{HOME}/.config/btop",
            "nvim": f"{HOME}/.config/nvim",
            "hypr": f"{HOME}/.config/hypr",
            "nwg-dock-hyprland": f"{HOME}/.config/nwg-dock-hyprland",
            "waybar": f"{HOME}/.config/waybar",
            "paru": f"{HOME}/.config/paru",
            "declarative_package": f"{HOME}/.config/declarative_package",
            "fastfetch": f"{HOME}/.config/fastfetch",
            "gtk-2.0": f"{HOME}/.config/gtk-2.0",
            "gtk-3.0": f"{HOME}/.config/gtk-3.0",
            "neofetch": f"{HOME}/.config/neofetch",
            "rofi": f"{HOME}/.config/rofi",
            "picom": f"{HOME}/.config/picom",
            "qt5ct": f"{HOME}/.config/qt5ct",
            "qt6ct": f"{HOME}/.config/qt6ct",
            "yay": f"{HOME}/.config/yay",
            "yazi": f"{HOME}/.config/yazi",
            "dunst": f"{HOME}/.config/dunst",
            "cava": f"{HOME}/.config/cava",
            "flameshot": f"{HOME}/.config/flameshot",
            "xsettingsd": f"{HOME}/.config/xsettingsd",
            "mimeapps.list": f"{HOME}/.config/mimeapps.list",
            "user-dirs.dirs": f"{HOME}/.config/user-dirs.dirs",
            "user-dirs.locale": f"{HOME}/.config/user-dirs.locale",
        },
        # -------------
        ".local": {
            "bin": f"{HOME}/.local/bin",
            "plank_themes": f"{HOME}/.local/share/plank",
        },
        # -------------
        ".themes": f"{HOME}/.themes",
        # -------------
        "Pictures": {
            "mcrfScins": f"{HOME}/Pictures/mcrfScins",
            "profile": f"{HOME}/Pictures/profile",
            # "screenshots": f"{HOME}/Pictures/screenshots",
            # "wallpapers": f"{HOME}/Pictures/wallpapers",
        },
        # -------------
        # "Videos": f"{HOME}/Videos",
        ".viebrc": f"{HOME}/.viebrc",
        ".zshrc": f"{HOME}/.zshrc",
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
