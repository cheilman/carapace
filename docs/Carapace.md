Carapace
========

It's like a shell, okay?

```
~/.carapace/
    |- CARAPACE            <- marker file; findCarapace looks for this
    |- bundles/
    |   |- base/
    |- modules/            <- symlinks only, generated
    |- install/
    |- generated/
    |   |- intermediate/
    |- backup/
    |- docs/
    |   |- templates/
    |- prereqs/            <- per-platform package manifests
    |- tests/              <- Dockerfiles for testing installs
    |- zshrc-update
~/.host/
    |...
~/.path-carapace
~/bin/carapace/            <- all module bin/ symlinks land here
```

Components
----------

### CARAPACE

A marker file whose presence indicates a Carapace installation.  `findCarapace`
looks for it when guessing where Carapace lives.  Don't delete it.

### bundles

Bundles are groups of modules related in purpose.  This allows different module-sets to be stored in separate repositories (such as for work-related settings in a company that requires use of a private git server).  The modules in each bundle folder are symlinked into the `modules/` folder.

Modules are the main content of the Carapace system (see [Module Documentation](Module.md) for more details).  Modules within this folder will be evaluated in lexicographical order.  A common practice is prefixing each module name with a two digit number (`10MyModule`) to more precisely define inclusion and execution order.

#### bundles/base

This bundle contains the standard set of functionality included with Carapace.

### modules

NOTE: No modules should live in this folder, each module should be part of a bundle.

The modules defined here are evaluated in lexicographical order during installation to build out the final shell system.

### install

There is a folder of scripts to assist with installation in `$HOME/.carapace/install/`.  These will manage the installation process.

### generated

Many files are generated from module-level components.  These all live in the `$HOME/.carapace/generated/` folder.

### backup

If installation would overwrite any existing files (usually with symlinks), the original file will be saved in `$HOME/.carapace/backup` and suffixed with a timestamp.

### docs

Carapace system documentation is stored in this folder.

#### docs/templates

Documentation that will be symlinked or copied on install (such as crontab headers and `.host` readmes).

### prereqs

Per-platform manifests of the packages a fully-populated host is expected to
have — Homebrew formulae, casks, and the leaves installed on request, one
directory per platform (`Darwin-Meta`, `WSL-Ubuntu-Meta`, and so on).  These are
reference material for rebuilding a machine, not something the installer
consumes.

Not to be confused with a *bundle's* `prereqs` file, which is a list of required
commands that installation does check.  See [Bundle Documentation](Bundle.md#prereqs).

### tests

Dockerfiles for exercising a clean install on a platform you don't have handy.

### zshrc-update

This is the script that runs on each login (symlinked to `$HOME/.zshrc`).  It
locates the Carapace installation and sources the generated zshrc file.  It also
supports profiling: set `ZPROF=true` before starting a shell and `zsh/zprof`
output will be printed at the end of startup.

Carapace resolution order:

1. `findCarapace` on the `PATH`
2. `$HOME/bin/carapace/findCarapace`
3. `$HOME/.carapace` (if it contains a `CARAPACE` marker file)

Note: this script does *not* auto-update Carapace.  Run `carapace-update
--install` by hand (or from cron) to pull and reinstall.

### `$HOME/.host` Files

The `$HOME/.host` folder contains files specific to this host.  Nothing in here is tracked by Carapace, and all files are optional.  If a file does exist, it will be referenced/included by the installation process.

See [Host](Host.md) and [Host Config](Host-Config.md) readmes for more details.

### ~/.path-carapace

This file contains a source-able path setting that is built over the course of initialization.  If you're having trouble with some executables (such as i3 running audio commands, etc.), your script may want to source this file to get an updated, valid path.

### Environment Variables

Set in every interactive shell:

Variable   | Contents
---------- | --------
`CARAPACE` | Absolute path to the Carapace root (usually `$HOME/.carapace`)

Set only during installation, inside the install scripts:

Variable                          | Contents
--------------------------------- | --------
`CARAPACE_GENERATED`              | `$CARAPACE/generated`
`CARAPACE_GENERATED_INTERMEDIATE` | `$CARAPACE/generated/intermediate` — where files are built before being swapped into place
`CARAPACE_INDENT`                 | Current indent prefix used by `carapace-message`
`CARAPACE_MODULES`                | Comma-separated `bundle/module` names installed so far.  **NOTE:** because each module runs in its own process, this only accumulates within a single script; it does not reach the interactive shell, where it is always empty.  See [TODO](TODO.md).

Set while a module's `zshrc` fragment is being evaluated, and cleared afterwards:

Variable                       | Contents
------------------------------ | --------
`CARAPACE_CURRENT_MODULE`      | `bundle/module`
`CARAPACE_CURRENT_MODULE_PATH` | Absolute path to the module directory

Installation
------------

### Installation Order

`carapace-install` runs these steps in order:

1. Create `~/bin/carapace`, `~/.config`, `~/.ssh` (0700), `~/.host/{config,config/login_certs,modules,bin}`, and `generated/intermediate`.
2. Seed `~/.host/README.md` and `~/.host/config/README.md` from `docs/`.
3. Link the install scripts into `~/bin/carapace/`.
4. Copy each `docs/templates/*-template` into `generated/intermediate/generated-*` and stamp it with a UTC build date.
5. Remove broken symlinks from `modules/`.
6. For each directory in `bundles/`, then `~/.host/modules` (as bundle `HOST`): link its modules into `modules/` as `<modulename>-<bundlename>`, and check the bundle's `prereqs` file.
7. For each directory in `modules/` in lexicographic order: run `carapace-install-module`.
8. Append the trailer to `generated-zshrc` and clear the module variables.
9. Delete `generated/generated*` and move `intermediate/*` into place.
10. Link the generated files to their homes and install the crontab.

A failing module does not stop the install; failures are collected and reported
at the end, and `carapace-install` exits 1.

### Generated Files

Built in `$CARAPACE/generated/intermediate/` and swapped into
`$CARAPACE/generated/` at the end of a successful install:

| Generated file         | Linked to                               | Built from module |
|------------------------|-----------------------------------------|-------------------|
| `generated-crontab`    | installed via `crontab`                 | `special/crontab` |
| `generated-gitconfig`  | `~/.gitconfig`                          | `special/gitconfig` |
| `generated-gitignore`  | `~/.gitignore`                          | `special/gitignore` |
| `generated-hgrc`       | `~/.hgrc`                               | `special/hgrc` |
| `generated-hgignore`   | `~/.hgignore`                           | `special/hgignore` |
| `generated-i3config`   | `~/.i3/config` (only if `~/.i3` exists) | `special/i3config` |
| `generated-profile`    | `~/.profile`                            | `special/profile` |
| `generated-ssh_config` | `~/.ssh/config`                         | `special/ssh_config` |
| `generated-ssh_rc`     | `~/.ssh/rc`                             | `special/ssh_rc` |
| `generated-vimrc`      | `~/.vimrc`                              | `special/vimrc` |
| `generated-zshrc`      | sourced by `zshrc-update`               | `zshrc` |

Other files that modules write into `generated/` and that are **not** cleared on
reinstall:

- `carapace-minimal.tar.gz` — built by `99minimal`
- `fortune-timestamp`, `fortune-timestamp_now` — `run-infrequently` bookkeeping for `97fortunes`
- `carapace-update-timestamp*` — orphaned; see [TODO](TODO.md)
