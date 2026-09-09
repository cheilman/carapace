Carapace Bundles
================

What makes up a bundle?
-----------------------

A bundle is simply a grouped collection of modules.

Bundle Structure
----------------

```
mybundle/
 |- prereqs      <- optional
 |- 10mod1
 |- 20mod2
 |- 30mod3
 ...
```

The idea is that bundles can be separate repositories and cloned into the
systems that matter.  A common usage is a company-based bundle stored in a
company-only git repo, isolating any proprietary details.

Modules are linked into `$CARAPACE/modules/` under a munged name:
`<module directory>-<bundle name>`.  So `bundles/base/50git` becomes
`modules/50git-base`, and `~/.host/modules/30meta` becomes `modules/30meta-HOST`.

Two consequences:

- Two bundles may ship a module with the same name without colliding.
- Ordering across bundles is by the numeric prefix, not by bundle.  `10foo-work`
  is processed before `50git-base`.

The munged name is also what appears in installer output and in
`CARAPACE_MODULES`, rendered as `bundle/module` (`base/git`, `HOST/meta`).

### prereqs

A bundle may contain a `prereqs` file at its root: one command name per line,
`#` for comments, blank lines ignored.  Each is checked with `which` during
installation.  Missing commands produce a warning but do **not** fail the
install — the bundle's modules are still processed.

You can re-run the check for every bundle at any time with
`carapace-check-prereqs`.

### `~/.host/modules` is a bundle

`carapace-install` treats `$HOME/.host/modules` as a bundle named `HOST`, using
exactly the mechanics above.  It is processed after every bundle in `bundles/`,
but its modules still interleave by numeric prefix.  Nothing in `~/.host` is
tracked by Carapace, which makes it the right home for machine-specific or
private content.

See the [Host Documentation](Host.md) for the rest of `~/.host`.

What does the module installation process look like?
----------------------------------------------------

1. Loop through each bundle in shell order
2. Check if there are any modules that are linked into this bundle that no longer exist, if so remove them
3. Link all modules from this bundle into the module root
4. If the bundle has a `prereqs` file, check it

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
