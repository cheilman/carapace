Host Config Directory
=====================

The `~/.host/config` folder is used by [Carapace](https://github.com/cheilman/carapace) to manage host-specific settings for the shell and modules.

This list is intended to be **exhaustive**: if a flag is not listed here, nothing
reads it.  Add an entry when you add a flag, so this file stays worth trusting.

Flags/Files
-----------

### disable\_goproxy

If present, sets `GOPROXY` to `direct` and removes references to `https://proxy.golang.org`.  Useful for restrictive corporate environments that block Google's proxy.

Read by `10go` (`zshrc`, `install`).

### gitrepos

Defines the search paths and depths for dynamically discovering git repositories.  Eventually this will be in some kind of format, but currently the file is just directly sourced.  It should contain calls to `add_git_repo_search_path` as:

```bash
add_git_repo_search_path "$HOME/.carapace" 3
add_git_repo_search_path "$HOME/prj" 3
...
```

Read by `50git/zshrc`.

### skip\_goutils

Some locations (Amazon, Meta) don't allow installing go modules/binaries from github.  If this flag is set this will skip installing any go utilities.  :sadface:

Read by `50goutils/update` and `60sysdash/update`.

### support\_manual\_go\_install

If we can't determine a supported pre-installed `go` version, and this file exists, then we will attempt to download `go` from the official Google repository and install it locally.

If this fails, or this file does not exist, then we may end up with no `go` installation.

Read by `10go/update`.

### sysdash

Sourced to configure the idle-screen dashboard.  Contains shell assignments:

- `SYSDASH_REPO_SEARCH_PATHS` -- override the repo list; falls back to `GIT_REPO_SEARCH_PATH` configured above.
- `SYSDASH_WEATHER_LOCATION` -- what city or zip code to display weather from.

Read by `30base/bin/idle`.

**NOTE:** `60sysdash/zshrc` does *not* currently load this file — the load is
commented out with a `TODO`.  See [TODO](TODO.md).

Not currently implemented
-------------------------

These were real once.  Nothing reads them today.  They are kept here so the
intent isn't lost and so nobody re-adds them assuming they work.  Each has an
entry in [TODO](TODO.md).

### auto\_update\_carapace

*Intended:* if present, carapace automatically runs `carapace-update`
periodically at startup (every 9 days).

*Actual:* no code reads this flag.  `zshrc-update` does not check for updates at
all, and `generated/carapace-update-timestamp` has been an empty orphan since
2023-10-11.  The machinery it would use (`30base/bin/run-infrequently`) still
exists and is used by `97fortunes`.

### check\_kerberos

*Intended:* `carapaceprompt` and other things check for the presence of an active
kerberos ticket, and display accordingly.

*Actual:* there is no `carapaceprompt` in `bundles/base` — the prompt is
Powerlevel10k (`40p10k` + `40zgenom`), which knows nothing about this flag.

### check\_midway

*Intended:* as `check_kerberos`, for midway certificates.

*Actual:* same — the prompt it configured no longer exists.

### login\_certs/

*Intended:* `carapaceprompt` had built-in support for Kerberos and Midway
tickets, plus a pluggable system for other login flags to appear on the prompt.
Any executable file in the `login_certs/` folder would be run, and if it had
non-empty output it would be added to the prompt.

*Actual:* nothing runs these.  `carapace-install` still creates the directory.
Powerlevel10k supports custom prompt segments cleanly, so this is worth porting
rather than deleting outright.
