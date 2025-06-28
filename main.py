#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-


from core.paths.handler import paths_handler
from core.cli import Cli
from modules.colors import Col
import sys


def main():
    cli = Cli()
    conf = cli.get_config()

    paths_handler()
    conf.generate()
    cli.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Col.PURPLE.value}\n\n\n     ~~> cancel  ^^ {Col.RESET.value}")
        sys.exit()
