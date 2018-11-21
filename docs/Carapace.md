Carapace
========

It's like a shell, okay?

```
~/.carapace/
    |- bundles/
        |- base/
    |- modules/
    |- install/
    |- generated/
    |- backup/
    |- docs/
    |   |- templates/
    |- zshrc-update
~/.host/
    |...
~/.path-carapace
```

Components
----------

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

### zshrc-update

This is the script that will be run on each login (symlinked to `$HOME/.zshrc`).  It checks for Carapace updates, and then executes the generated zshrc file.

### `$HOME/.host` Files

The `$HOME/.host` folder contains files specific to this host.  Nothing in here is tracked by Carapace, and all files are optional.  If a file does exist, it will be referenced/included by the installation process.

See [Host](Host.md) and [Host Config](Host-Config.md) readmes for more details.

### ~/.path-carapace

This file contains a source-able path setting that is built over the course of initialization.  If you're having trouble with some executables (such as i3 running audio commands, etc.), your script may want to source this file to get an updated, valid path.

### Environment Variables

A few environment variables are set by the Carapace system:

Variable           | Contents
------------------ | --------
`CARAPACE`         | The path to the `$HOME/.carapace` directory
`CARAPACE_MODULES` | A comma separated list of modules (minus the numeric prefix) that have been successfully installed.

Installation
------------

### Generated Files

The following files may be generated in `$HOME/.carapace/generated`:

- `generated-crontab`
- `generated-gitconfig`
- `generated-gitignore`
- `generated-i3config`
- `generated-profile`
- `generated-ssh_config`
- `generated-vimrc`
- `generated-zshrc`

