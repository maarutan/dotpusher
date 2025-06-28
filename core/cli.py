from pathlib import Path
from argparse import ArgumentParser
from .config import Config
from .paths.list import JSONC_CONFIG
from .config_handler import ConfigHandler
import argcomplete


class Cli:
    def __init__(self) -> None:
        self.parser = ArgumentParser(description="Dotpusher CLI")

        self.parser.add_argument(
            "-c",
            "--config",
            type=Path,
            default=Path(JSONC_CONFIG).expanduser(),
            help="Path to config file",
        )

        self.parser.add_argument(
            "-s", "--sync", action="store_true", help="Sync dotfiles"
        )

        self.parser.add_argument(
            "-p", "--push", action="store_true", help="Push dotfiles"
        )

        self.parser.add_argument(
            "-f", "--force", action="store_true", help="Force push"
        )

        argcomplete.autocomplete(self.parser)
        self.args = self.parser.parse_args()
        self._conf_handler = None  # lazy init

    def get_config(self) -> Config:
        return Config(self.args.config)

    def get_config_handler(self) -> ConfigHandler:
        if self._conf_handler is None:
            self._conf_handler = ConfigHandler(self.get_config())
        return self._conf_handler

    def run(self) -> None:
        if self.args.sync:
            from .commands.sync import Sync

            Sync().sync()
        elif self.args.push:
            from .commands.push import Push

            Push().push(force=self.args.force)
        else:
            self.parser.print_help()
