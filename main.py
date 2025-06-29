#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-


from core.paths.handler import paths_handler
from core.cli import Cli
from modules.colors import Col
import sys
import threading


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
        print(
            f"\n\n{Col.YELLOW.value}[warn]{Col.RESET.value} {Col.RED.value}Canceled by user :D {Col.RESET.value}"
        )
        print(f"{Col.PURPLE.value}\n     ~~> cancel  ^^ {Col.RESET.value}")
        sys.exit(130)
    finally:
        for t in threading.enumerate():
            if t is not threading.main_thread():
                try:
                    t.join(timeout=0.1)
                except Exception:
                    pass
