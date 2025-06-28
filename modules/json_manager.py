import json
from dataclasses import dataclass
from pathlib import Path
from modules import FileManager


@dataclass
class JsonManagerArgs:
    path: Path


class JsonManager(JsonManagerArgs):
    def __init__(self, path: Path):
        super().__init__(path)
        self.fm = FileManager(self.path)

    def _strip_comments(self, raw: str) -> str:
        import io

        output = io.StringIO()
        inside_str = False
        prev_char = ""

        for line in raw.splitlines():
            new_line = ""
            i = 0
            while i < len(line):
                char = line[i]

                if char == '"' and prev_char != "\\":
                    inside_str = not inside_str

                if (
                    not inside_str
                    and char == "/"
                    and i + 1 < len(line)
                    and line[i + 1] == "/"
                ):
                    break

                new_line += char
                prev_char = char
                i += 1

            output.write(new_line + "\n")

        return output.getvalue()

    def read(self) -> dict:
        with open(self.path, "r", encoding="utf-8") as f:
            raw = f.read()
            clean = self._strip_comments(raw)
            return json.loads(clean)

    def write(self, data: dict, indent: int = 2) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)

    def get_data(self) -> dict:
        if self.path.exists():
            return self.read()
        return {}

    def update_json(self, data: dict) -> None:
        existing = self.get_data()
        existing.update(data)
        self.write(existing)
