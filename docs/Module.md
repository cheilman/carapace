Carapace Modules
================

What makes up a module?
-----------------------

A module is a releated collection of scripts, binaries, configuration, etc.  Files are managed in a specific way:

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
 |- update
 |- zshrc
```

### bin/

This folder contains binaries.  The contents will be symlinked to `$HOME/bin/Carapace/`

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

### dotfiles/

This folder should contain files or directories that live as hidden files in `$HOME`.  Each entry in `dotfiles/` will be symlinked into `$HOME/`, with a period pre-pended.  For example: `ln -s $HOME/.carapace/modules/mymod/dotfiles/mygoat $HOME/.mygoat`.

### special/

This folder contains specially handled configuration files.  Specifically:

#### crontab

Module `crontab` files will be appended to the generated Carapace-wide `generated-crontab` file, and then installed using `crontab`.

#### gitconfig

Module `gitconfig` files will be appended to the generated Carapae-wide `generated-gitconfig` file, and then symlinke to `$HOME/.gitconfig`.

#### gitignore

Module `gitignore` files will be appended to the generated Carapae-wide `generated-gitignore` file, and then symlinke to `$HOME/.gitignore`.

#### profile

Module `profile` files will be appended to the generated Carapace-wide `generated-profile` file, and executed whenever `$HOME/.profile` is.

#### ssh_config

Module `ssh_config` files will be appended to the generated Carapace-wide `generated-ssh_config` file, and symlinked to `$HOME/.ssh/config`.

#### vimrc

Module `vimrc` files will be appended to the generated Carapace-wide `generated-vimrc` file, and symlinked to `$HOME/.vimrc`.

### zshrc

Module `zshrc` files will be appended to the generated Carapace-wide `generated-zshrc` file, and executed whenever `$HOME/.zshrc` is.

Two environment variables will be available to you:

- `CARAPACE_CURRENT_MODULE` -- The name of the current module
- `CARAPACE_CURRENT_MODULE_PATH` -- The path to the current module's folder

Remember that relative paths likely won't work correctly, as your code will be executing from the generated file.  Use the `CARAPACE_CURRENT_MODULE_PATH` to locate other files from your module.  Also note that these environment variables won't persist after your zshrc script execution, so they will either be wrong or unavailable if you try to use them later (such as in functions).

### install

An optional script that is executed on Carapace installations or upgrades.  It should be idempotent enough to be run on every upgrade without causing problems.  The install script serves two purposes:

- It serves as a test to see if this module should be installed or not.  A non-zero return value means that this module will not be processed further (during this installation).
- It allows configuration/setup/dependency/etc. processing that Carapace does not support by default.  For example:
    - Cloning/updating a git repo for a dependency
    - Building/installing/updating a go program
    - Installing apt packages
    - etc.
- It is important that if this module requires external updates (such as a git repository), that the install script run those updates.

#### Usage:

`install <module dir> <generated dir>`

What does the module installation process look like?
----------------------------------------------------

1. If the `install` file exists, execute it, along with the path to the generated files folder.
    1. If the exit code is non-zero, skip this module
2. If the `install` file was successful, or did not exist, continue with module installation
3. Append the `zshrc` file to the `generated-zshrc` file.
4. Symlink all the `bin/` files to the correct location
5. Symlink all the `dotfiles/` files to the correct location (following the [description in that section](#dotfiles)).
6. Symlink all the `config/` files to the correct location (following the [description in that section](#config)).
7. Process each of the `special/` files [as necessary](#special).
8. Add the module name to the list of installed modules (see [Environment Variables](Carapace.md#Environment-Variables) section in the [Carapace documentation](Carapace.md))

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
