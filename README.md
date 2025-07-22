<table align="center">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/f340a733-1423-4095-84e9-99c6f8aa2f32" width="2600"/></td>
    <td>
        <p style="font-size:20px">
          <strong>dotpusher</strong> - is a mini script written in Python that allows you to copy
          [dotfiles] declaratively to the result directory and then push them to a
          remote repository without imperative intervention.
        </p>
    </td>
  </tr>
</table>

<h3 align="left">━━━━━━━━━━➤ DOTPUSHER</h3>
<h3 align="left">━━━━━━━━━━━━━━━━━━━➤</h3>

<div align="center">
  <h6>(c) 2025 maaru.tan / Marat Arzymatov. All Rights Reserved.</h6>
</div>

### 📎 Links

- [What is `dotpusher`](#-what-is-dotpusher)
- [Video Example](#-dotpusher-demo-walkthrough-as-shown-in-the-video)
- [Dependencies](#-dependencies)
- [Installation](#-installation)

---

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

### 🔑 Fields Description

- **url**: Remote Git repository for pushing dotfiles.
- **branch**: Git branch to push to.
- **dirname**: Folder name under `result_location`.
- **result_location**: Where synced files are collected.
- **assets**: Path for static files like README, LICENSE.
- **noconfirm**: Uses `default_commit_message` automatically.
- **stop_when_warned**: Seconds to pause on warnings.
- **blacklist**: Files/folders to ignore when copying.
- **resources**: Dotfiles structure to replicate.

---

## 🚀 Usage & CLI Options

```bash
# Synchronize only
$ dotpusher -s

# Sync + Git push
$ dotpusher -p

# Force push (⚠️ destructive)
$ dotpusher -p -f

# Use custom config
$ dotpusher -c <path-to-config>
$ dotpusher -c <path-to-config> ( -s | -p | -p -f )

# Display help
$ dotpusher -h
```

---

## 🧱 Directory Structure Example

For:

```json
"dirname": "dotfiles",
"result_location": "~/.config/dotpusher/dist",
```

Structure:

```
~/.config/dotpusher/dist/
├── dotfiles/
    ├── .git
│   ├── .themes/
│   ├── Pictures/
│   ├── .local/
│   │   └── bin/
│   └── ...
├── assets/
│   └── dotfiles/
│       ├── LICENSE
│       ├── README.md
│       └── .gitignore
```

---

## 📁 Assets Directory

Derived from the config field:

```json
"assets": "{result_location}/assets/{dirname}"
```

Resolves to:

```
~/.config/dotpusher/dist/assets/dotfiles/
```

Store:

- README.md
- LICENSE
- .gitignore
- Any static helpers

---

## 🧠 Best Practices

- Prefer absolute paths for single files
- `--push` for daily syncs
- `--push --force` for full overwrites
- Use separate configs per system
- Always check `dotpusher -h`

---

## 📦 Dependencies

- Python 3.11+
- Git

---

## 📦 Installation

### From AUR:

```bash
yay -S dotpusher
```

### Manual:

```bash
# Clone the repository
git clone https://github.com/maarutan/dotpusher.git
cd dotpusher
```

```bash
sudo ./install.sh
# To uninstall:
sudo ./uninstall.sh
```

---

## 🎥 Dotpusher Demo Walkthrough (as shown in the video)

**Example video:**

https://github.com/user-attachments/assets/8e081933-2f7b-4bb0-8c67-c18c6e7fb519

### Steps:

1. Show GitHub repo
2. Delete local contents
3. Push empty state to GitHub
4. Configure `config.jsonc`
5. Run `dotpusher -p`
6. Files sync to `~/.config/dotpusher/dist`
7. Git push completes to target branch

Result: your repo is fully version-controlled with desired structure.

---

## 📝 License

See the [`LICENSE`](./LICENSE) file for terms.

---

> Built with ❤️ by [maarutan](https://github.com/maarutan)<br/>
> Automate your dotfiles. Stay declarative. Be consistent.
