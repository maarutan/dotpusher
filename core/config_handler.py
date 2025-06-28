from pathlib import Path
from typing import Any, Optional
from modules import (
    JsonManager,
    FileManager,
)


class ConfigHandler:
    def __init__(self, config: Any) -> None:
        self.jm = JsonManager
        self.fm = FileManager
        self.p = Path
        self.conf = config

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        try:
            value = self.conf.get_option(key)
            return default if value in (None, "", {}) else value
        except Exception:
            return default

    def get_url(self) -> str:
        return self.get("url", "")

    def get_branch(self) -> str:
        return self.get("branch", "")

    def get_noconfirm(self) -> bool:
        return self.get("noconfirm", False)

    def get_result_location(self) -> Path:
        path = self.get("result_location", "")
        absolute_path = self.p(path).expanduser()
        self.fm(absolute_path).if_not_exists_create()
        return self.p(absolute_path)

    def get_dirname(self) -> str:
        name = self.get("dirname", "")
        parent_dir = self.p(self.get_result_location())
        target_dir = parent_dir / name
        self.fm(target_dir).if_not_exists_create()
        return name

    def get_blacklist(self) -> list:
        return self.get("blacklist", [])

    def get_assets(self) -> Path:
        path = self.get("assets", "")
        path = str(path).format(
            result_location=self.get_result_location(),
            dirname=self.get_dirname(),
        )
        self.fm(self.p(path)).if_not_exists_create()
        return self.p(path)

    def get_warn_timeout(self) -> float:
        return self.get("stop_when_warned", 0.0)

    def get_resources(self) -> dict[str, list[str]]:
        return self.get("resources", {})

    def get_default_commit_message(self) -> str:
        return self.get("default_commit_message", "")

    def get_result_dir(self) -> Path:
        path = self.get_result_location() / self.get_dirname()
        fm = self.fm(path)

        if not fm.is_exists():
            created_path = fm.if_not_exists_create()
            if created_path is None:
                raise RuntimeError(f"Failed to create result dir: {path}")
            return created_path

        return path
