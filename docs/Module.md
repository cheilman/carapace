Carapace Modules
================

What makes up a module?
-----------------------

A module is a related collection of scripts, binaries, configuration, etc.  Files are managed in a specific way:

Module Structure
----------------

All files and folders are optional.

```
mymod/
 |- bin/
 |- config/
 |- dotfiles/
 |- special/
 |- install
 |- post-install
 |- update
 |- zshrc
```

### bin/

This folder contains binaries.  The contents will be symlinked into the `$HOME/bin/carapace/` folder.

### config/

The contents of this folder will be linked into the system configuration folder at `$HOME/.config`.  Assume we have a module such as:

```
mymod/
 |- config/
     |- goat/
     |   |- mygoat
     |- othergoat
```

The file `config/othergoat` will be symlinked into the `$HOME/.config` folder, replacing whatever was there previously (backing it up).  Ex: `ln -s $HOME/.carapace/modules/mymod/config/othergoat $HOME/.config/othergoat`.

If the folder `$HOME/.config/goat` *does not* exist, then it will be symlinked directly into Carapace.  Ex: `ln -s $HOME/.carapace/modules/mymod/config/goat $HOME/.config/goat`.

However, if the folder `$HOME/.config/goat` *does* exist, then only the contents of `config/goat` will be symlinked in.  Ex: `ln -s $HOME/.carapace/modules/mymod/config/goat/mygoat $HOME/.config/goat/mygoat`.  The `goat` folder within `$HOME/.config` will remain a real folder.

This is what lets two modules contribute into the same `$HOME/.config` subdirectory.

### dotfiles/

This folder should contain files or directories that live as hidden files in `$HOME`.  Each entry in `dotfiles/` will be symlinked into `$HOME/`, with a period pre-pended.  For example: `ln -s $HOME/.carapace/modules/mymod/dotfiles/mygoat $HOME/.mygoat`.

### special/

This folder contains specially handled configuration files.  Specifically:

#### crontab

Module `crontab` files will be appended to the generated Carapace-wide `generated-crontab` file, and then installed using `crontab`.

#### gitconfig

Module `gitconfig` files will be appended to the generated Carapace-wide `generated-gitconfig` file, and then symlinked to `$HOME/.gitconfig`.

#### gitignore

Module `gitignore` files will be appended to the generated Carapace-wide `generated-gitignore` file, and then symlinked to `$HOME/.gitignore`.

#### hgrc

Module `hgrc` files will be appended to the generated Carapace-wide `generated-hgrc` file, and then symlinked to `$HOME/.hgrc`.

#### hgignore

Module `hgignore` files will be appended to the generated Carapace-wide `generated-hgignore` file, and then symlinked to `$HOME/.hgignore`.

#### i3config

Module `i3config` files will be appended to the generated Carapace-wide `generated-i3config` file, which is symlinked to `$HOME/.i3/config` **only if `$HOME/.i3` already exists**.

#### profile

Module `profile` files will be appended to the generated Carapace-wide `generated-profile` file, and executed whenever `$HOME/.profile` is.

These fragments must be **POSIX sh**, not zsh — `$HOME/.profile` is sourced by `/bin/sh` as well as by the `01pre` module's zshrc.

#### ssh_config

Module `ssh_config` files will be appended to the generated Carapace-wide `generated-ssh_config` file, and symlinked to `$HOME/.ssh/config`.

#### ssh_rc

Module `ssh_rc` files will be appended to the generated Carapace-wide `generated-ssh_rc` file, and symlinked to `$HOME/.ssh/rc`.

#### vimrc

Module `vimrc` files will be appended to the generated Carapace-wide `generated-vimrc` file, and symlinked to `$HOME/.vimrc`.

#### A note on expansion

`crontab` and `i3config` fragments are processed before being appended:

- lines beginning with `##` are dropped (use them for notes you don't want in the output)
- `$HOME` is replaced with the literal home directory path

Every other `special/` file is appended verbatim.

### zshrc

Module `zshrc` files will be appended to the generated Carapace-wide `generated-zshrc` file, and executed whenever `$HOME/.zshrc` is.

Two environment variables will be available to you:

- `CARAPACE_CURRENT_MODULE` -- The name of the current module
- `CARAPACE_CURRENT_MODULE_PATH` -- The path to the current module's folder

Remember that relative paths likely won't work correctly, as your code will be executing from the generated file.  Use the `CARAPACE_CURRENT_MODULE_PATH` to locate other files from your module.  Also note that these environment variables won't persist after your zshrc script execution, so they will either be wrong or unavailable if you try to use them later (such as in functions).  If a function needs the path, capture it into your own variable at definition time:

```zsh
typeset -g _MYMOD_DIR="${CARAPACE_CURRENT_MODULE_PATH}"
mytool() { "${_MYMOD_DIR}/bin/tool" "$@" }
```

This file runs on **every** interactive shell start — in every tmux pane, every ssh session, every terminal tab.  Keep it cheap, and guard anything that depends on an external command actually being installed.

### install

An optional script that is executed on Carapace installations or upgrades.  It should be idempotent enough to be run on every upgrade without causing problems.  The install script serves two purposes:

- It serves as a test to see if this module should be installed or not.  A non-zero return value means that this module will not be processed further (during this installation).

    **NOTE:** at present a non-zero `install` exit is also counted as a module *failure* — it is printed in red, listed in the failure summary, and makes `carapace-install` exit 1.  There is currently no way for a module to opt out quietly.  Because `carapace-install-module` runs under `set -e`, the script's own "Skipping ..." branch is never reached.  See [TODO](TODO.md).

- It allows configuration/setup/dependency/etc. processing that Carapace does not support by default.  For example:
    - Cloning/updating a git repo for a dependency
    - Building/installing/updating a go program
    - Installing apt packages
    - etc.
- It is important that if this module requires external updates (such as a git repository), that the install script run those updates.

The working directory is **not** the module directory.  Recompute it from the arguments, as every module in the tree does:

```zsh
moduledir="${1:-${0:a:h}}"
generated="${2:-/dev/null}"
```

#### Usage:

`install <module dir> <generated dir>`

### update

An optional script executed by `carapace-update` (not by `carapace-install`).
This is where a module refreshes anything it fetched from outside Carapace:
cloning or pulling a vendored git repo, reinstalling a Go binary, rebuilding a
cached artifact.

Unlike `install`, it receives only the module directory.  It must be idempotent
and safe to run on a machine where the dependency has never been installed.

A non-zero exit marks the module as failed for this update pass and is reported
at the end of `carapace-update` (with the same caveat as `install`, above).

#### Usage:

`update <module dir>`

### post-install

An optional script that is executed after the rest of the module installation has finished.  It should be idempotent enough to be run on every upgrade/install without causing problems.  This script allows you to initialize anything that requires the symlinks to be set up already.  It operates similarly to the install script.

#### Usage:

`post-install <module dir> <generated dir>`

Ordering
--------

Modules are processed in lexicographic order of their directory name, across
all bundles.  The convention is a two-digit numeric prefix followed by a
lowercase name.  Ranges currently in use in `bundles/base`:

| Range | Meaning | Examples |
|-------|---------|----------|
| `01`–`09` | Bootstrap.  `$PATH`/`$FPATH` helpers, locale, shell options. | `01pre`, `02brew` |
| `10`–`29` | Language toolchains and editors. | `10go`, `11vim` |
| `30`–`39` | Core shell: aliases, functions, completion config. | `30base` |
| `40`–`44` | Prompt and plugin manager.  Anything that adds to `$fpath` belongs here or below. | `40zgenom`, `40p10k` |
| `45`–`69` | Tools.  The bulk of the bundle. | `50git`, `50fzf` |
| `70`–`89` | Optional / desktop / niche. | `70grc`, `70conky` |
| `90`–`98` | Late overrides, including fragments that undo what a plugin did. | `95tmux`, `98vim` |
| `99` | Final.  Path cache flush, history options. | `99post` |

Two modules may share a number; ties break on the name.

### Ordering fragments

Some content has to land after a later module has run — for example, undoing an
alias that oh-my-zsh sets, or appending a final block to a generated file.  The
convention is a second module named for the first but at a higher priority:
`45tmux` is paired with `95tmux`, `11vim` with `98vim`.

Keep these small and comment why they exist, so the next reader doesn't delete
one as redundant.

What does the module installation process look like?
----------------------------------------------------

1. If the `install` file exists and is executable, run it with the module directory and the generated files folder.
    1. If the exit code is non-zero, skip the rest of this module.
2. Append the `zshrc` file to the `generated-zshrc` file.
3. Symlink all the `bin/` files into `$HOME/bin/carapace/`.
4. Remove any symlinks in `$HOME/bin/carapace/` that point at files in this module that no longer exist.
5. Symlink all the `dotfiles/` files to the correct location (following the [description in that section](#dotfiles)).
6. Remove any symlinks in `$HOME` that point at files in this module that no longer exist.
7. Remove any symlinks in `$HOME/.config` (one and two levels deep) that point at files in this module that no longer exist.  This happens *before* the config install so the "already linked?" test below behaves correctly.
8. Symlink all the `config/` files to the correct location (following the [description in that section](#config)).
9. Process each of the `special/` files [as necessary](#special).
10. If the `post-install` file exists and is executable, run it.
11. Add the module name to the list of installed modules (see [Environment Variables](Carapace.md#environment-variables) section in the [Carapace documentation](Carapace.md))

The pruning steps (4, 6, 7) are why renaming or deleting a file inside a module
cleans up after itself, and why a module can't leave stale links behind.

A module script that exists but is **not executable** is skipped with a warning.
`chmod +x` is part of creating one.

How can I communicate to the user during installation?
------------------------------------------------------

The `carapace-message` executable will echo a message to the user.  You can also color messages.

Usage: `carapace-message <color> <message>`

Color is either one of the following, or `bold` and one of the following:

- black, red, green, yellow, blue, magenta, cyan, white

Examples:

- `carapace-message "cyan" "Hello world!"`
- `carapace-message "boldgreen" "Everything is a-okay!"`
- `carapace-message "boldred" "We're hosed!"`
