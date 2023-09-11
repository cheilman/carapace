Host Directory
==============

The `~/.host/minimal` folder is used by [Carapace Minimal](https://github.com/cheilman/carapace/bundles/base/50minimal/carapace-minimal/docs/CarapaceMinimal.md)
to allow per-host settings that are not managed by the global repository.

```
~/.host/
  |- minimal/
     |- bashrc-pre
     |- bashrc-post
  |- pretty-hostname
  |- timezone
```

Components
----------

### pretty-hostname

Allows most of the Carapace systems to display a nicer hostname than `hostname -s` or whatever.

- If this is an executable file, the file will be run and the first line of output used as the hostname.
- If this file is readable, the file will be read and the first line used as the hostname.

### timezone

If this file exists, it will override the timezone set in Carapace.

### minimal/

This folder contains overrides and extra hooks for host-specific settings that are not persisted in source control.

#### bashrc-pre

Runs *before* any carapace bashrc code.

#### bashrc-post

Runs *after* any Carapace bashrc code.

