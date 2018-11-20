Host Config Directory
==============

The `~/.host/config` folder is used by [Carapace](https://github.com/cheilman/carapace) to manage host-specfic settings for the shell and modules.  The list below is non-exhaustive.

Flags/Files
-----------

### check\_kerberos

If present, carapaceprompt and other things will check for the presence of an active kerberos ticket, and display accordingly.

### check\_midway

If present, carapaceprompt and other things will check for the presence of an active midway certificate, and display accordingly.

### gitrepos

Defines the search paths and depths for dynamically discovering git repositories.  Eventually this will be in some kind of format, but currently the file is just directly sourced.  It should contain calls to `add_git_repo_search_path` as:

```bash
add_git_repo_search_path "$HOME/.carapace" 3
add_git_repo_search_path "$HOME/prj" 3
...
```

### sysdash

Defines environment variables that control [sysdash](https://github.com/cheilman/sysdash) configuration.  Eventually these lines will be loaded as environment variables, but currently it just is directly sourced.

Configuration settings here *should* be defined in the sysdash README, but they aren't :/.

- `SYSDADSH_REPO_SEARCH_PATHS` -- if you want to define different search paths for the repos specified by sysdash.  Otherwise falls back to `GIT_REPO_SEARCH_PATH` configured above.
- `SYSDASH_TWITTER_ACCT_[123]` -- what three twitter accounts to display tweets from
- `SYSDASH_TWITTER_CONSUMER_(KEY|SECRET)` and `SYSDASH_TWITTER_ACCESS_TOKEN(_SECRET)?` -- credentials for connecting to the Twitter API
- `SYSDASH_WEATHER_LOCATION` -- What city or zip code to display weather from.

