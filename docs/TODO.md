Carapace To-Do
==============

Carried over from the old `README.md` migration checklist, plus gaps found in
the 2026-09-08 review.

Migration leftovers
-------------------

These are the last unmigrated pieces from `cahhome`.  All have been open since
2023; if they're still open in another year they should just be closed.

- [ ] `docker-files` — the container definitions from the old dockerfiles repo.
      (The `docker` module itself migrated; only the dockerfiles did not.)
- [ ] `lyntin` — mud client config.
- [ ] Fix `cahhome-limited`.

Known discrepancies
-------------------

Places where the code and the documentation disagree, or where a documented
feature is not implemented.  Each is described in more detail where it lives.

- [ ] **`CARAPACE_MODULES` is always empty.**  `carapace-install-module` exports
      it, but it is a separate process, so the value never reaches the parent
      installer or the interactive shell.  Either populate it from
      `carapace-install` and emit an `export` line into `generated-zshrc`, or
      remove the concept.  See [Carapace.md](Carapace.md#environment-variables).

- [x] ~~**A module's `install` script cannot opt out quietly.**~~  Fixed: module
      scripts may exit `$CARAPACE_SKIP` (42) to mean "not applicable on this
      host", which is skipped quietly.  Any other non-zero exit is a real
      failure.  `10go`, `97toybox` and `50goutils` now use it.

- [ ] **`auto_update_carapace` is documented but not implemented.**  Nothing
      reads the flag, and `generated/carapace-update-timestamp` has been a
      0-byte orphan since 2023-10-11.  The tooling to implement it
      (`run-infrequently`) still exists and is used by `97fortunes`.  See
      [Host-Config.md](Host-Config.md#not-currently-implemented).

- [ ] **The prompt login-status flags are orphaned.**  `check_kerberos`,
      `check_midway` and the `login_certs/` directory all describe
      `carapaceprompt`, which no longer exists — the prompt is Powerlevel10k
      (`40p10k` + `40zgenom`).  Either drop them or port `login_certs` to a p10k
      custom segment.  See [Host-Config.md](Host-Config.md#not-currently-implemented).

Candidates for removal
----------------------

Zero usage in ~16k lines of shell history on the Linux devserver, but plausibly
still used on a Mac or the WSL host.  Check on those machines, then delete.

- [ ] `40powerline` — tmux-powerline; superseded by `40p10k` for the shell prompt,
      but the tmux status line may still use it.
- [ ] `50stormy` — `~/.config/stormy`.
- [ ] `50taskwarrior` — taskrc plus `mytasks`, `tasksync`, `watchmytasks`.
- [ ] `70conky` — conky config; desktop only.
- [ ] `50neofetch` — 4 uses; cheap to keep, listed for completeness.

Also deferred, for reasons other than cross-host uncertainty:

- [ ] `70grc` — zero usage, but deleting it was not authorised.  Its
      `accept-line` widget has been optimised instead (the config glob is
      hoisted out of the hot path).
- [ ] `90mist`, `90wreck`, `90nethack`, `50souls` — personal, not "standard
      functionality", and `bundles/base` is published.  `90mist/special/ssh_config`
      contains port-forward topology for a personal host.  Moving them to a
      separate bundle would break the other machines that expect them in `base`,
      so this needs a plan rather than a delete.
- [ ] Trim the `40zgenom` plugin list.  `z`, `bgnotify`, `copybuffer`,
      `copypath`, `copyfile` and `colorize` are unused, but each costs under
      0.3 ms so the behavioural risk outweighs the win.  `ssh-agent` has already
      been dropped (it fought with `50ssh`).

Weight
------

- [ ] **`11vim` is 26 MB**, most of it `ale`'s `test/test-files/` — fixtures for
      elixir, racket, puppet, drush, swift and other languages that aren't in
      use.  Vundle has no shallow-clone option, so fixing this properly means
      moving to a plugin manager that does (vim-plug, packer, or vim 8 native
      packages).  `Vundle.vim` itself is now cloned `--depth 1`.

Other
-----

- [ ] **`60sysdash` was deleted**; its `zshrc` body had been commented out with a
      `TODO` since 2023.  `~/.host/config/sysdash` is still read by
      `30base/bin/idle`, which is the only live consumer.
