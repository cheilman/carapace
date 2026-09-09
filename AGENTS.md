AGENTS.md — Working on Carapace
===============================

Guide for AI coding agents (Claude Code, Codex, Antigravity, Muse, Cursor, Aider,
or any other) working in this repository. Written to be tool-agnostic: it
assumes only a shell, a file editor, and the ability to read.

This file is the single source of truth. If your tool looks for a
differently-named instruction file, add a one-line pointer to this one rather
than a copy — `CLAUDE.md` in this repo is exactly that. Duplicated instruction
files drift within a month.

---

## 1. What Carapace is

Carapace manages a user's shell and dotfiles. It is a **build system, not a
runtime**. Small config fragments scattered across *modules* are concatenated,
in a defined order, into whole config files, which are then symlinked into
`$HOME`.

```
bundles/*/<NNname>/zshrc   ──concat──►  generated/generated-zshrc  ──sourced by──►  ~/.zshrc
bundles/*/<NNname>/special/gitconfig ─►  generated/generated-gitconfig ──symlink──►  ~/.gitconfig
bundles/*/<NNname>/bin/*   ──symlink──►  ~/bin/carapace/*
bundles/*/<NNname>/dotfiles/foo ─sym──►  ~/.foo
bundles/*/<NNname>/config/foo   ─sym──►  ~/.config/foo
```

The single most important consequence: **nothing takes effect until you run
`carapace-install`.** Editing a module file and opening a new shell does
nothing.

### The three layers

| Layer | Path | Tracked in git? | Purpose |
|---|---|---|---|
| **Bundle** | `bundles/<name>/` | `base` yes; others are separate repos or gitignored | A group of modules with a shared theme. `base` ships with Carapace. |
| **Module** | `bundles/<bundle>/<NNname>/` | with its bundle | One coherent unit of functionality. |
| **Host** | `~/.host/` | never | Machine-specific overrides. `~/.host/modules/` is treated as a bundle named `HOST`. |

---

## 2. Repository map

```
CARAPACE            Marker file.  findCarapace looks for this; do not delete.
zshrc-update        Symlinked to ~/.zshrc.  Locates $CARAPACE, sources the generated zshrc.
README.md           Landing page.
AGENTS.md           This file.
CLAUDE.md           Pointer to this file.

bundles/
  base/             The standard bundle.  ~39 modules.
    prereqs         One command name per line; checked (warning only) at install.
  <other>/          Cloned in per-host; see bundles/.gitignore for the known names.

modules/            GENERATED.  Symlinks only: <module>-<bundle> -> the real module dir.
                    Never create anything here by hand.

install/            The installer.  See §6.
generated/          GENERATED.  Never edit; edit the module and reinstall.
  intermediate/     Scratch space during a build.
backup/             Files displaced by symlinks, suffixed with a UTC date.
docs/               System documentation.
  templates/        Header text prepended to each generated file.
  TODO.md           Known gaps, including code/doc discrepancies.
prereqs/            Per-platform package manifests (Homebrew leaves/casks).
tests/              Dockerfiles for exercising a clean install.
proposed-changes/   Untracked scratch space for review output.  Gitignored;
                    may not exist on a fresh clone.
```

---

## 3. Rules

These are the ones that cause real damage when broken.

1. **Never edit anything in `generated/`.** It is deleted and rebuilt by
   `carapace-install`. Find the module that contributed the text (each block is
   wrapped in `#### Included from: <bundle>/<module>` with the source path) and
   edit that.

2. **Never edit `~/.zshrc`, `~/.gitconfig`, `~/.vimrc`, `~/.profile`,
   `~/.hgrc`, `~/.ssh/config`, `~/.ssh/rc`, or the user's crontab.** All are
   symlinks or installed copies owned by Carapace. Changes are silently
   discarded on the next install.

3. **Never put a module directly in `modules/`.** It is generated. Put it in a
   bundle, or in `~/.host/modules/`.

4. **Machine-specific or private content goes in `~/.host/modules/`, not
   `bundles/base/`.** `bundles/base` is published at
   `github.com/cheilman/carapace`. Hostnames, port forwards, internal URLs,
   employer-specific tooling, and anything resembling a credential do not
   belong there.

5. **Run `carapace-install` after any change, and open a *new* shell to test.**
   Reloading the current one gives misleading results.

6. **Every module script must be executable.** `install`, `post-install` and
   `update` are silently skipped with a warning if the executable bit is
   missing. `chmod +x` is part of creating the file.

7. **Ask before running `carapace-uninstall`.** It runs
   `find -P $HOME -maxdepth 20 -xdev -type l -lname "$CARAPACE/*" -delete`.

---

## 4. Module anatomy

Directory name is `<NN><name>` — two digits of priority, then a lowercase name.
Everything in a module is optional.

```
<NN><name>/
  zshrc          Appended to generated-zshrc.  Runs in every interactive shell.
  bin/*          Symlinked into ~/bin/carapace/ (which is on $PATH).
  dotfiles/foo   Symlinked to ~/.foo.
  config/foo     Symlinked to ~/.config/foo.  See §4.3.
  special/*      Fragments for other generated files.  See §4.2.
  install        Run at install time.  Args: <module dir> <generated dir>.
  post-install   Run after symlinks exist.  Args: <module dir> <generated dir>.
  update         Run by carapace-update only.  Args: <module dir>.
```

### 4.1 Priority numbers

Modules are processed in lexicographic order of `<NN><name>`, across all
bundles. Conventions currently in use in `base`:

| Range | Meaning | Examples |
|---|---|---|
| `01`–`09` | Bootstrap. `$PATH`/`$FPATH` helpers, locale, shell options. | `01pre`, `02brew` |
| `10`–`29` | Language toolchains and editors. | `10go`, `11vim` |
| `30`–`39` | Core shell: aliases, functions, completion config. | `30base` |
| `40`–`44` | Prompt and plugin manager. **Anything that adds to `$fpath` must be below 45.** | `40zgenom`, `40p10k` |
| `45`–`69` | Tools. The bulk of the bundle. | `50git`, `50fzf`, `60sysdash` |
| `70`–`89` | Optional / desktop / niche. | `70grc`, `70conky` |
| `90`–`98` | Late overrides, including `-post` fragments that undo what a plugin did. | `95tmux`, `98vim` |
| `99` | Final. Path cache flush, history options. | `99post` |

Two modules may share a number; ties break on the name.

If you need a fragment to land *after* a module you can't modify (typically to
undo an oh-my-zsh alias), the convention is a second small module at a higher
priority — `45tmux` is paired with `95tmux`, `11vim` with `98vim`. Keep those
tiny and comment why they exist.

### 4.2 `special/` files

Each is appended to the correspondingly-named generated file:

| File | Generated file | Installed to | Comment char |
|---|---|---|---|
| `crontab` | `generated-crontab` | `crontab` command | `#` |
| `gitconfig` | `generated-gitconfig` | `~/.gitconfig` | `#` |
| `gitignore` | `generated-gitignore` | `~/.gitignore` | `#` |
| `hgrc` | `generated-hgrc` | `~/.hgrc` | `#` |
| `hgignore` | `generated-hgignore` | `~/.hgignore` | `#` |
| `i3config` | `generated-i3config` | `~/.i3/config` (only if `~/.i3` exists) | `#` |
| `profile` | `generated-profile` | `~/.profile` | `#` |
| `ssh_config` | `generated-ssh_config` | `~/.ssh/config` | `#` |
| `ssh_rc` | `generated-ssh_rc` | `~/.ssh/rc` | `#` |
| `vimrc` | `generated-vimrc` | `~/.vimrc` | `"` |

`crontab` and `i3config` go through `append-with-expansion`, which differs from
the others:

- lines starting with `##` are **stripped** (use them for notes)
- `$HOME` is replaced with the literal home directory

Everything else is appended byte-for-byte.

`special/profile` must be **POSIX sh**, not zsh — it is sourced by `/bin/sh` as
well as by `01pre/zshrc`.

### 4.3 `config/` directory merging

- `config/foo` (a file) → symlinked to `~/.config/foo`.
- `config/foo/` (a directory) and `~/.config/foo` **does not exist** → the whole
  directory is symlinked.
- `config/foo/` and `~/.config/foo` **is a real directory** → each *entry* is
  symlinked individually; the directory stays real.

This lets two modules contribute into the same `~/.config` subdirectory.

### 4.4 Writing a `zshrc` fragment

Two variables are available **while your fragment runs** and are cleared
afterwards:

- `CARAPACE_CURRENT_MODULE` — `bundle/module`, e.g. `base/git`
- `CARAPACE_CURRENT_MODULE_PATH` — absolute path to the module directory

Because everything is concatenated into one file, relative paths are meaningless
and the current directory is the user's. Always use
`$CARAPACE_CURRENT_MODULE_PATH`:

```zsh
#!zsh
#
# What this module does, and why.
#

source "${CARAPACE_CURRENT_MODULE_PATH}/helper.sh"
add_path_back "${CARAPACE_CURRENT_MODULE_PATH}/bin"
```

The two variables **do not survive** into functions you define — by the time a
function is called, they have been reset to empty. Capture the value at
definition time:

```zsh
# WRONG - $CARAPACE_CURRENT_MODULE_PATH is empty when the user calls this
mytool() { "${CARAPACE_CURRENT_MODULE_PATH}/bin/tool" "$@" }

# RIGHT
typeset -g _MYMOD_DIR="${CARAPACE_CURRENT_MODULE_PATH}"
mytool() { "${_MYMOD_DIR}/bin/tool" "$@" }
```

Helper functions defined by `01pre` and available to every later module:

```zsh
add_path_front <dir>    # prepend to $PATH  (no-op if not a directory)
add_path_back  <dir>    # append to $PATH
add_fpath_front <dir>   # prepend to $FPATH
add_fpath_back  <dir>   # append to $FPATH
```

**Guard everything on the tool existing.** A fragment that unconditionally
aliases a command breaks the shell on every host lacking that command:

```zsh
(( $+commands[eza] )) && alias ls='eza'
```

**This file runs on every shell start.** Before adding a `$(...)`, a `source
<(...)`, or a loop that forks, know what it costs. See §8.

### 4.5 `install` vs `post-install` vs `update`

| | `install` | `post-install` | `update` |
|---|---|---|---|
| Run by | `carapace-install` | `carapace-install` | `carapace-update` |
| When | Before symlinks | After symlinks | Before a reinstall |
| Args | `<moduledir> <generateddir>` | `<moduledir> <generateddir>` | `<moduledir>` |
| Typical use | Detect a dependency; generate a file the `zshrc` will read | Anything needing the symlinks in place (`vim +PluginInstall`) | `git pull` a vendored repo; `go install` a binary |

All three must be **idempotent** — they run on every install/update. All three
recompute their own module directory rather than trusting `$PWD`:

```zsh
moduledir="${1:-${0:a:h}}"
generated="${2:-/dev/null}"
```

**Known sharp edge:** `carapace-install-module` and `carapace-update-module` run
under `set -e`. A non-zero exit from your script aborts the wrapper immediately,
before its "Skipping ..." branch runs, so the module is reported to the user as a
**failure** and `carapace-install` exits 1. There is currently no way to opt out
quietly. If you need conditional installation, prefer detecting inside the
`zshrc` fragment.

Use `carapace-message <color> <text>` for user-facing output — it handles
indentation. Colors: `black red green yellow blue magenta cyan white`, each
optionally prefixed with `bold`.

---

## 5. Common tasks

### Add a module to `base`

```bash
cd ~/.carapace/bundles/base
mkdir -p 55mytool/bin
cat > 55mytool/zshrc <<'EOF'
#!zsh
#
# mytool - short description of why this exists
#

(( $+commands[mytool] )) || return 0

export MYTOOL_CONFIG="${HOME}/.config/mytool"
alias mt='mytool --colour'
EOF
chmod +x 55mytool/bin/* 2>/dev/null   # if you added any
carapace-install
```

Pick the number from the table in §4.1. If it touches `$fpath`, it must be
below 45.

### Add machine-specific config

Same shape, but in `~/.host/modules/<NNname>/`. It becomes part of the `HOST`
bundle automatically. Nothing there is tracked by git.

### Add a new bundle

```bash
git clone <repo> ~/.carapace/bundles/mybundle
carapace-install
```

Add the directory name to `bundles/.gitignore` so the parent repo ignores it.
Optionally add a `prereqs` file at the bundle root listing required commands.

### Change something in a generated file

Find the owning module:

```bash
grep -n "Included from" ~/.carapace/generated/generated-zshrc
# ...then find the block containing the line you care about
```

Each block header also names the exact source file. Edit that, reinstall.

### Remove a module

```bash
git rm -r bundles/base/50oldthing
carapace-install     # prunes the modules/ symlink and any bin/dotfile links
```

The installer removes symlinks that point into the now-missing module. Files it
displaced earlier stay in `backup/`.

---

## 6. The install pipeline

`install/carapace-install` (zsh, `set -e`):

1. Create `~/bin/carapace`, `~/.config`, `~/.ssh` (0700), `~/.host/{config,config/login_certs,modules,bin}`, `generated/intermediate`.
2. Seed `~/.host/README.md` and `~/.host/config/README.md` from `docs/`.
3. Link `carapace-install`, `carapace-update`, `carapace-uninstall`, `carapace-check-prereqs`, `findCarapace` into `~/bin/carapace/`.
4. Copy `docs/templates/*-template` into `generated/intermediate/generated-*`, stamped with a UTC build date.
5. Remove broken symlinks from `modules/`.
6. For each bundle in `bundles/`, then `~/.host/modules` as `HOST`: link its modules into `modules/` as `<module>-<bundle>`, check the bundle's `prereqs`.
7. For each directory in `modules/`, lexicographically: `carapace-install-module`.
8. Append the trailer to `generated-zshrc`, clear the module variables.
9. `rm generated/generated*`, then `mv intermediate/* generated/`.
10. Symlink the generated files into place; install the crontab.

Failures are collected and reported at the end; the install continues past them
and exits 1.

`install/carapace-update`: `git pull --recurse-submodules` on the root and on
each bundle that is its own repo, then runs each module's `update`. With
`--install` it finishes by calling `carapace-install`.

### Helper scripts

| Script | Purpose |
|---|---|
| `carapace-install-bundle <dir> <moduleroot> <generated> [name]` | Link one bundle's modules; check `prereqs`. |
| `carapace-install-module <name> <dir> <generated>` | The per-module pipeline. |
| `carapace-update-module <name> <dir>` | Run one module's `update`. |
| `carapace-redirect <src> <dst>` | Idempotent symlink with backup to `backup/`. Use this rather than `ln -s`. |
| `carapace-message <color> <text>` | Indented, coloured output. |
| `carapace-prereqs <file>` | Check a list of commands. |
| `carapace-check-prereqs` | Run the check for every bundle. |
| `findCarapace` | Locate the installation. |

---

## 7. Verifying a change

Run all of these after any non-trivial edit.

```bash
# 1. Install cleanly
carapace-install; echo "exit=$?"

# 2. Interactive shell starts without errors
zsh -i -c 'exit'

# 3. Startup time did not regress
for i in 1 2 3; do /usr/bin/time -f "%e s" zsh -i -c exit 2>&1 | tail -1; done

# 4. Completion set did not shrink
zsh -i -c 'print ${#_comps}'

# 5. Your fragment landed where you expected
grep -n "Included from" ~/.carapace/generated/generated-zshrc

# 6. No dangling symlinks
find ~ -maxdepth 3 -xtype l 2>/dev/null | grep -i carapace

# 7. Function-level profile, if something got slower
ZPROF=true zsh -i -c exit
```

For a clean-machine test, use the Docker image in `tests/ubuntu/`.

---

## 8. Performance

`generated-zshrc` runs on every shell start — in every tmux pane, every ssh
session, every terminal tab. Treat it as a hot path.

**Budget:** a `zshrc` fragment should add **under 5 ms**. If yours doesn't, cache
the expensive part.

Measure before and after:

```zsh
zmodload zsh/datetime
t=$EPOCHREALTIME; <the thing>; printf "%.1f ms\n" $(( ($EPOCHREALTIME-t)*1000 ))
```

Rules of thumb:

| Don't | Do |
|---|---|
| `eval "$(tool shellenv)"` | Cache the output to a file, regenerate when the tool is newer than the cache |
| `source <(tool --init zsh)` | Same |
| `which foo` / `command -v foo` in a loop | `(( $+commands[foo] ))` — no fork |
| `if [ $(...) ]` for existence checks | zsh conditionals and glob qualifiers |
| A second `compinit` | There must be exactly one, and it must be cached |
| Work inside a `precmd`/`preexec`/widget | Hoist it to startup, or don't do it |

The `$(...)` and `[ ... ]` idioms in older modules predate this guidance. Match
the file you're editing rather than rewriting it wholesale, but don't add new
ones.

---

## 9. Environment-specific gotchas

**Aliases leak into agent tool calls.** This user's interactive zsh aliases
`cat` to `bat` and `date` to `gdate`, and neither is installed on every host. If
your agent harness sources the user's profile, `"$(cat file)"` can silently
evaluate to the empty string while the surrounding command proceeds. Prefer:

```bash
"$(< file)"        # shell builtin, no external command
command cat file   # bypass the alias
```

Better still, use your file-reading tool instead of shelling out.

**Read `docs/` first.** `docs/Carapace.md`, `docs/Bundle.md`, `docs/Module.md`,
`docs/Host.md`, `docs/Host-Config.md` are the authority on intended behaviour.
`docs/TODO.md` lists the places where the code and the documentation still
disagree — check it before trusting a feature you haven't seen work.

---

## 10. Style

- Shell scripts: `#!/usr/bin/env zsh`. `zshrc` fragments start with `#!zsh` (a
  marker, not a shebang — they are sourced, never executed).
- `special/profile` fragments must be POSIX sh.
- Two-space indent in shell. Tabs appear in a few older files; don't propagate
  them.
- Comment blocks use the existing form:

  ```zsh
  #
  # What this section does
  #
  ```

- Every module's `zshrc` opens with a comment saying what the module is for.
  A reader scrolling 1,500 lines of `generated-zshrc` needs that.
- Quote variable expansions. Paths on these machines contain `.` and `-`, and
  at least one host has spaces.
- Prefer `carapace-redirect` over `ln -s`; it backs up what it displaces.
- Prefer `carapace-message` over `echo` in install scripts.

---

## 11. Before you finish

- [ ] `carapace-install` exits 0
- [ ] A new `zsh -i` starts with no errors or warnings
- [ ] Startup time did not regress (§7)
- [ ] Nothing was written to `generated/`, `modules/`, or `~/.zshrc` by hand
- [ ] New scripts are executable
- [ ] Nothing host-specific, private, or credential-shaped landed in `bundles/base/`
- [ ] Docs updated if you changed behaviour the docs describe
