<table align="center">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/f340a733-1423-4095-84e9-99c6f8aa2f32" width="2600"/></td>
    <td>
        <p size="20px">
          <strong>dotpusher</strong> - is a mini script written in Python that allows you to copy
          [dotfiles] declaratively to the result directory and then push them to a
          remote repository without imperative intervention.
        </p>
    </td>
  </tr>
</table>

<p align="left">
  <h3>━━━━━━━━━━➤DOTPUSHER</h3>
  <h3>━━━━━━━━━━━━━━━━━━━➤<h3>
</h3h3>

<div align="center">
  <h6> (Copyright (c) 2025 maaru.tan \ Marat Arzymatov. All Rights Reserved.)</h6> <br>

### links

[What is `dotpusher`](What is Dotpusher)
[Vidoeo Example](Dotpusher Demo Walkthrough (as shown in the video))
[Installation](Installation)
[Dependencies](Dependencies)

<div align="left">
# 📚 Dotpusher – Full Wiki

## 📌 What is Dotpusher?

**Dotpusher** is a lightweight Python script that enables you to declaratively manage, sync, and version-control your dotfiles. It supports pushing to remote repositories, custom configurations, and dynamic directory structures.

    ---

## ⚙ Configuration File: `config.jsonc`

### Example Overview:

```json
{
  "url": "git@github.com:maarutan/dotfiles",
  "branch": "main",
  "dirname": "dotfiles",
  "result_location": "~/.config/dotpusher/dist",
  "assets": "{result_location}/assets/{dirname}",
  "noconfirm": true,
  "default_commit_message": "dotpusher",
  "stop_when_warned": 0.5,
  "blacklist": [".git", "__pycache__"],
  "resources": {
    "~/": ["Pictures", ".themes", ".local/bin"],
    "~/.config": ["nvim", "yazi", "~/Pictures/rose.png"]
  }
}
```

---

### 🔑 Fields

#### `url`

Remote Git repository for pushing dotfiles.

#### `branch`

Branch where files will be pushed.

#### `dirname`

Name of the target directory inside `result_location`.

#### `result_location`

Main output directory. This will be initialized as a Git repository (if not already).

#### `assets`

Subdirectory inside result location where you can add custom files like `README.md`, `.gitignore`, or a `LICENSE`.

#### `noconfirm`

If `true`, bypasses manual commit messages using `default_commit_message`.

#### `stop_when_warned`

Time (in seconds) to pause on warning or error messages, giving the user a chance to read them.

#### `blacklist`

List of files or directories that should not be copied into the result directory.

#### `resources`

Defines what should be copied and from where. Format:

```json
"<parent>": ["child1", "child2", ...]
```

Supports:

- Recursive copying
- Absolute and relative paths
- Nested directories (e.g., `.local/bin` will recreate `.local` in the result directory with `bin` inside)
- Direct file copies with absolute paths (e.g., `~/Pictures/rose.png`)

---

## 🚀 Usage & CLI Options

### Synchronization only

```bash
dotpusher -s / --sync
```

Copies files from your system to `result_location`, **no Git operations performed**.

### Synchronization + Push

```bash
dotpusher -p / --push
```

- Syncs files
- Initializes Git repo (if not exists)
- Pushes to remote defined in `url`

### Force Push

```bash
dotpusher -p -f / --push --force
```

- Re-clones the remote repo
- Overwrites contents
- Recommended for full refreshes (⚠️ destructive)

### Custom Config

```bash
dotpusher -c <path-to-config>
```

Allows using different configs for multiple repositories.

### Help & All Options

```bash
dotpusher -h
```

---

## 🧱 Directory Structure Example

If your config has:

```json
"dirname": "dotfiles",
"result_location": "~/.config/dotpusher/dist",
```

Then the final structure becomes:

```
~/.config/dotpusher/dist/
├── dotfiles/
├── .git
│   ├── .themes/
│   ├── Pictures/
│   ├── .local/
│   │   └── bin/
│   └── ...
└── assets/
└── dotfiles/
├── LICENSE
├── README.md
└── .gitignore
```

---

## 📦 Dependencies

- `Python 3.11+`
- `Git`

---

## 📦 Installation

### From AUR (Arch-based systems):

```bash
yay -S dotpusher
```

### Manual Installation

```bash
sudo ./install.sh
# Uninstall:
sudo ./uninstall.sh
```

---

## 📁 Assets Directory

Assets are dynamically determined using:

```json
"assets": "{result_location}/assets/{dirname}"
```

Which expands to something like:

```
~/.config/dotpusher/dist/assets/dotfiles/
```

Useful for storing:

- `.gitignore`
- `README.md`
- `LICENSE`
- Any other static or helper files for your dotfiles repo

---

## 🧠 Best Practices

- Use absolute paths when copying single files (e.g., `~/Pictures/rose.png`)
- Use `--push` for safe updates
- Use `--push --force` when you need a full reset
- Maintain separate configs for different systems or machines
- Always verify with `dotpusher -h`

---

</div>

## Dotpusher Demo Walkthrough (as shown in the video)

#### **For example**

https://github.com/user-attachments/assets/8e081933-2f7b-4bb0-8c67-c18c6e7fb519

In the video demonstration, I start by showing the GitHub repository. Then, I clear its contents locally — meaning I delete everything from the local copy of the repository. After that, I push the cleaned state back to GitHub, resulting in an empty repository.

---

### Configuration Overview

After resetting the repository, I navigate to the default configuration directory:

```
~/.config/dotpusher
```

Inside this directory, you'll find the default configuration file: `config.jsonc`. I briefly go over the structure of this configuration to give a high-level overview of how Dotpusher works.

---

### Running the Tool

I then run the command:

```
dotpusher -p
```

This command gathers the files and directories listed in the config and synchronizes them to the output directory defined in the configuration, which by default is:

```
~/.config/dotpusher/dist/
```

You can modify this output path in the configuration by changing the `dirname` field.

---

### Pushing to a Remote

Once the files are prepared, Dotpusher can push them to a remote Git repository (GitHub, for example). Just make sure the `url` is correctly specified in the config.

The push is done with:

```
git push <your-branch> --force
```

---

### Final Result

In the end, I show how all the files and directories defined in `config.jsonc` appear in the remote repository, structured and committed exactly as intended.

---

This process makes it easy to declaratively manage and version your dotfiles using Git.

</div>

## 📝 License

Licensed under the terms defined in your repository. For more, see the [`LICENSE`](./LICENSE) file.

---

> Built with ❤️ by [maarutan](https://github.com/maarutan)

> Automate your dotfiles. Stay declarative. Be consistent.
