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
