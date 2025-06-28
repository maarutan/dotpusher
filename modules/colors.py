from enum import Enum


class Col(str, Enum):
    """class Colors"""

    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    PURPLE = "\033[35m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE_TEXT = "\033[4m"
