Host Directory
==============

The `~/.host` folder is used by [Carapace](https://github.com/cheilman/carapace) to allow
per-host settings that are not managed by the global repository.

```
~/.host/
    |- bin/
    |- config/
        |- login_certs/
    |- modules/
    |- pretty-hostname
    |- timezone
```

Nothing in here is tracked by Carapace, which makes it the right home for
machine-specific or private content.

`carapace-install` creates the directories above if they're missing, and seeds
`~/.host/README.md` and `~/.host/config/README.md` as symlinks to this file and
to [Host Config](Host-Config.md).  Edit the originals in `docs/`, not the copies.

Components
----------

### bin

Host-specific executables can be added here.  This folder will be on the path, and will be have
the highest priority.

### config

Host-level configuration of the Carapace system (and modules).  The presence or absense of files
here, as well as the content, can affect Carapace module operation.

Options are described in the [Host Config Readme](Host-Config.md).

### modules

Host-specific modules can be created here according to the [Module Documentation](Module.md).  `~/.host/modules` is treated as a bundle named `HOST`, so its contents are linked and ordered exactly like any other bundle's — see [Bundle Documentation](Bundle.md).

### pretty-hostname

Allows most of the Carapace systems to display a nicer hostname than `hostname -s` or whatever.

- If this is an executable file, the file will be run and the first line of output used as the hostname.
- If this file is readable, the file will be read and the first line used as the hostname.

The consumer is `30base/bin/pretty-hostname`.

### timezone

If this file exists it is **sourced** by the shell instead of Carapace setting
its default (`America/New_York`).  It must therefore contain shell code, not a
bare zone name:

```sh
export TZ='Europe/Berlin'
```
