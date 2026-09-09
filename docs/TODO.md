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

- [ ] **A module's `install` script cannot opt out quietly.**
      `carapace-install-module` runs under `set -e`, so a non-zero exit from
      `install` aborts the wrapper before its "Skipping ..." branch can run.
      The module is skipped, but it is reported as a *failure* and
      `carapace-install` exits 1.  A dedicated "not applicable" exit code
      (checked with `|| err=$?` so `set -e` doesn't intercept it) would
      separate "doesn't apply here" from "broken".  Affects `post-install` and
      `update` the same way.  See [Module.md](Module.md#install).

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

- [ ] **`60sysdash` does not load its host config.**  The body of
      `60sysdash/zshrc` is commented out with a `TODO`.  The only live reader of
      `~/.host/config/sysdash` is `30base/bin/idle`.
