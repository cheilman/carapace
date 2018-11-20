Host Directory
==============

The `~/.host` folder is used by [Carapace](https://github.com/cheilman/carapace) to allow
per-host settings that are not managed by the global repository.

```
~/.host/
    |- bin/
    |- config/
    |- modules/
    |- timezone
```

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

Host-specific modules can be created here according to the [Module Documentation](Module.md), and will be linked in accordingly (as if `~/.host/` were a bundle).

### timezone

If this file exists, it will override the timezone set in Carapace.

