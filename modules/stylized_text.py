from .colors import Col


class StylizedText:
    def __init__(
        self, col: str = Col.RESET.value, content: str = "Enter content"
    ) -> None:
        self.font = self._fonts().get("calvin_s")
        if not self.font:
            raise ValueError(f"Font 'calvin_s' not found.")
        self.content = content
        self.col = col

    def _fonts(self) -> dict:
        return {
            "calvin_s": {
                "a": "┌─┐\n├─┤\n┴ ┴",
                "b": "┌┐ \n├┴┐\n└─┘",
                "c": "┌─┐\n│  \n└─┘",
                "d": "┌┬┐\n ││\n─┴┘",
                "e": "┌─┐\n├─ \n└─┘",
                "f": "┌─┐\n├┤ \n└",
                "g": "┌─┐\n│ ┬\n└─┘",
                "h": "┬ ┬\n├─┤\n┴ ┴",
                "i": "┬\n│\n┴",
                "j": " ┬\n │\n└┘",
                "k": "┬┌─\n├┴┐\n┴ ┴",
                "l": "┬  \n│  \n┴─┘",
                "m": "┌┬┐\n│││\n┴ ┴",
                "n": "┌┐┌\n│││\n┘└┘",
                "o": "┌─┐\n│ │\n└─┘",
                "p": "┌─┐\n├─┘\n┴  ",
                "q": "┌─┐ \n│─┼┐\n└─┘└",
                "r": "┬─┐\n├┬┘\n┴└─",
                "s": "┌─┐\n└─┐\n└─┘",
                "t": "┌┬┐\n │ \n ┴ ",
                "u": "┬ ┬\n│ │\n└─┘",
                "v": "┬  ┬\n└┐┌┘\n └┘",
                "w": "┬ ┬\n│││\n└┴┘",
                "x": "─┐ ┬\n┌┴┬┘\n┴ └─",
                "y": "┬ ┬\n└┬┘\n ┴ ",
                "z": "┌─┐\n┌─┘\n└─┘",
            },
        }

    def render(self) -> str:
        lines = [""] * 3
        for char in self.content:
            char_lines = self.font.get(char.lower(), "   \n   \n   ").split("\n")  # type: ignore
            for i in range(3):
                lines[i] += char_lines[i] + ""
        return "\n".join(lines)

    def __str__(self) -> str:
        try:
            return f"{self.col}" + self.render() + f"{Col.RESET.value}"
        except Exception:
            return "Error: no valid font"
