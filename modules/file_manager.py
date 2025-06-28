from pathlib import Path
from shutil import rmtree


class FileManager:
    """File Manager"""

    def __init__(self, path: Path) -> None:
        """initial path"""
        self.path = path

    def is_exists(self) -> bool:
        """check if path exists"""
        try:
            return Path(self.path).exists()
        except Exception as e:
            print(f"Error FileMnager (is_exists): {e}")
            return False

    def delete(self) -> None:
        """delete file or directory"""
        try:
            if not self.is_exists():
                return

            path = Path(self.path)

            if path.is_file():
                path.unlink()
            else:
                rmtree(path)

        except Exception as e:
            print(f"Error FileMnager (delete): {e}")

    def append(self, content: str) -> None:
        """append content in file"""
        try:
            with open(self.path, "a") as f:
                f.write(content)
        except Exception as e:
            print(f"Error FileMnager (append): {e}")

    def if_not_exists_create(self) -> None:
        try:
            if self.path.suffix:
                if not self.path.exists():
                    self.path.touch()
                    self.path.parent.mkdir(parents=True, exist_ok=True)
            else:
                if not self.path.exists():
                    self.path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Error in FileManager (if_not_exists_create): {e}")

    def write(self, content: str) -> None:
        try:
            with open(self.path, "w") as f:
                f.write(content)
        except Exception as e:
            print(f"Error FileMnager (write): {e}")

    def read(self):
        if not self.path.exists():
            return ""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error FileManager (read): {e}")
            return ""
