Carapace
========

It's like a shell, okay?

```
~/.carapace/
    |- modules/
    |- install/
    |- generated/
    |- backup/
    |- docs/
    |- zshrc
    |- profile
~/.host/
    |- config/
    |- zshrc-pre
    |- zshrc-post
    |- profile
    |- crontab
    |- sshconfig
```

Components
----------

### Modules

The modules are the main content of the Carapace system (see [Module Documentation](Module.md) for more details).  Modules within this folder will be evaluated in lexicographical order.  A common practice is prefixing each module name with a two digit number (`10MyModule`) to more precisely define inclusion and execution order.

### Install

There is a folder of scripts to assist with installation in `$HOME/.carapace/install/`.  These will manage the installation process.

### Generated

Many files are generated from module-level components.  These all live in the `$HOME/.carapace/generated/` folder.

### Backup

If installation would overwrite any existing files (usually with symlinks), the original file will be saved in `$HOME/.carapace/backup` and suffixed with a timestamp.

### Docs

Carapace system documentation is stored in this folder, along with documentation that will be symlinked or copied on install (such as crontab headers and `.host` readmes).

### zshrc

This is the script that will be run on each login (symlinked to `$HOME/.zshrc`).  It checks for Carapace updates, and then executes the generated zshrc file.

### profile

This is symlinked into the main `$HOME/.profile` and calls out to the generated profile file.

### `$HOME/.host` Files

The `$HOME/.host` folder contains files specific to this host.  Nothing in here is tracked by Carapace, and all files are optional.  If a file does exist, it will be referenced/included by the installation process.

#### `$HOME/.host/config` Settings

Host-level configuration of the Carapace system (and modules).  The presence or absense of files here, as well as the content, can affect Carapace module operation.  See the readme linked in this folder.

### Environment Variables

A few environment variables are set by the Carapace system:

Variable | Contents
-------- | --------
CARAPACE | The path to the `$HOME/.carapace` directory
CARAPACE_MODULES | A comma separated list of modules (minus the numeric prefix) that have been successfully installed.

Installation
------------
