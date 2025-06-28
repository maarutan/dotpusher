from typing import Optional, Tuple
from subprocess import PIPE, Popen, run, CalledProcessError


class Shell:
    def cmdline(
        self,
        command: str = "echo enter your command :D",
        Popens: bool = False,
        runs: bool = True,
        capture_output: bool = False,  # новый флаг для получения stderr
    ) -> Optional[str]:
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
                return f"Error (code {process.returncode}): {stderr.strip()}"
            return stdout.strip()

        elif runs:
            try:
                result = run(
                    command,
                    shell=True,
                    text=True,
                    stdout=PIPE,
                    stderr=PIPE,
                    check=True,
                )
                return result.stdout.strip()
            except CalledProcessError as e:
                if capture_output:
                    return f"Error (code {e.returncode}): {e.stderr.strip()}"
                return f"Error: command failed with code {e.returncode}"

        else:
            return "Error: cmdline invalid arguments :("
