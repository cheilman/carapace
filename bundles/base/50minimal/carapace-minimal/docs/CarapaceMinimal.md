Carapace Minimal
================

Carapace Minimal is a bash-based, minimal installation for hosts that:
1. Don't support zsh
2. Don't have connectivity to github/internet
3. Don't require the full feature set of Carapace
4. Have limited disk space (minimal install takes up 7.4M as of 2020-05-19)

How does it work?
-----------------

Every time Carapace is installed or updated, a special tarball is built that contains a carapace-minimal install.  It is stored in the generated files folder under $CARAPACE/generated/carapace-minimal.tar.gz  When carapace-minimal is installed on a host, this tarball is copied over, extracted, and then linked up to the correct rc files.

### How do I use it?

To install carapace-minimal on a host, run:

```
$ carapace-minimal-install-on-host [-f] <hostname>
```

This will do the following things:
1. Verify the tarball exists
2. Check that the version on the host is missing or different than the local version.
    - This can be overridden by the -f (force) flag.
3. Create the necessary directory structure on the remote host.
4. Untar the carapace-minimal install to $HOME/.carapace/minimal
5. Display version/metadata now on the remote host
6. Run the local installation script ($HOME/.carapace/minimal/install) to build the symlinks.

Configuration Layout
--------------------

```
carapace-minimal/ ($HOME/.carapace/minimal/ on installed systems)
  |- bin/
  |- docs/
      |- <these files>
  |- dotfiles/
  |- special/
  |- metadata
  |- version
```

### bin/

This folder contains binaries.  The contents will be symlinked to `$HOME/bin/carapace-minimal/`, and added to the $PATH.

### dotfiles/

This folder should contain files or directories that live as hidden files in `$HOME`.  Each entry in `dotfiles/` will be symlinked into `$HOME/`, with a period pre-pended.  For example: `ln -s $HOME/.carapace/minimal/dotfiles/bashrc $HOME/.bashrc`.

### special/

This folder contains specially handled configuration files.  Specifically:

#### gitconfig

Minimal `gitconfig` files will be appended to the generated Carapae-wide `generated-gitconfig` file, and then symlinked to `$HOME/.gitconfig`.

#### hgrc

Module `hgrc` files will be appended to the generated Carapae-wide `generated-hgrc` file, and then symlinked to `$HOME/.hgrc`.

#### vimrc

Module `vimrc` files will be appended to the generated Carapace-wide `generated-vimrc` file, and symlinked to `$HOME/.vimrc`.

### metadata

This contains metadata specific to the installation of carapace-minimal that is on the host.  Current format is key:value pairs, one per line.

### version

A directory hash is built when the tarball is generated, and inserted into the version file.  This is used to determine if an update on a host is required or not.

TODOs
-----

- [ ] Have a method of pulling host data into the tarball for auto-pushing to server


