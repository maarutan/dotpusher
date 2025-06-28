from pathlib import Path
from modules import (
    JsonManager,
    FileManager,
)


class Config:
    def __init__(
        self,
        config: Path,
    ):
        self.config = config
        self.jm = JsonManager(self.config)
        self.fm = FileManager
        self.indent = 2

    def generate(self) -> None:
        try:
            r = self.fm(self.config).read()
            if not r or r == False and self.fm(self.config).is_exists():
                self.fm(self.config).write(
                    """//
//    ┌┬┐┌─┐┌┬┐┌─┐┬ ┬┌─┐┬ ┬┌─┐┬─┐    ==\\
//     │││ │ │ ├─┘│ │└─┐├─┤├┤ ├┬┘  =======>
//    ─┴┘└─┘ ┴ ┴  └─┘└─┘┴ ┴└─┘┴└─    ==/
//
// copyright (c) 2025 maarutan \\ marat arzymatov. all rights reserved.
// ----------------------------------------------------------------------->
//
{
  "url": "<git@github.com:><UserName>/<Repo>",          // Remote repository URL for your dotfiles
  "branch": "<Branch>",                                 // Branch to use for push/pull operations

  "dirname": "<DirectoryName>",                         // Target directory name inside result_location
  "result_location": "~/.config/dotpusher/dist",        // Final output path where all resources will be gathered

  "assets": "{result_location}/assets/{dirname}",       // Optional: path to assets or additional files (e.g., README.md)

  "noconfirm": true,                                    // Run without asking for confirmations
  "default_commit_message": "dotpusher",                // Default git commit message
  "stop_when_warned": "0.5",                            // Delay (in seconds) when a warning occurs; set to 0 to disable

  "blacklist": [          // What will be ignored when items are copied
    ".git",               // Exclude .git directories from all operations
    "__pycache__"         // Exclude Python bytecode caches
  ],

  "resources": {                      // Directories to copy
    "~/": [
      // "Pictures",                  // Copies the ~/Pictures directory into the result root directory
      // ".themes"                    // Copies the ~/.themes directory into the result root directory
      // ".zshrc"                     // Uncomment to copy ~/.zshrc into the result root directory
    ],

    "~/.config": [
      // "nvim",                      // Copies the ~/.config/nvim directory
      // "~/Pictures",                // Copies the entire ~/Pictures directory into ~/.config/
      // "~/Pictures/nixos_tan.jpg"   // Copies only nixos_tan.jpg into ~/.config/
    ],

    "/etc": [
      // "ly/config.ini",             // Interpreted as a relative path: result/etc/ly/config.ini
      // "/etc/ly/config.ini"         // Interpreted as an absolute file path: copied into result/etc/config.ini
    ]

    // and more ...
  }
}"""
                )
        except Exception as e:
            print(f"Config.generate: {e}")

    def get_option(self, option) -> str:
        try:
            return self.jm.get_data()[option]
        except Exception as e:
            print(f"Config.get_option: {e}")
            return ""
