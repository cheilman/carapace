Carapace
========

Modular shell/dotfiles infrastructure.

Install:

    git clone https://github.com/cheilman/carapace.git ~/.carapace
    ~/.carapace/install/carapace-install

Update:

    carapace-update --install

See [full documentation](docs/Carapace.md).  Working on this with an AI agent?
Start at [AGENTS.md](AGENTS.md).

Layout
------

| Path | What |
|------|------|
| `bundles/` | Content, grouped into bundles of modules.  `base/` ships with Carapace; others are cloned in per-host. |
| `modules/` | Generated symlinks — do not put anything here by hand. |
| `install/` | The installer and its helpers. |
| `generated/` | Built config files.  Do not edit; edit the module and reinstall. |
| `docs/` | System documentation, plus the templates that head each generated file. |
| `prereqs/` | Per-platform package manifests (Homebrew leaves, casks). |
| `tests/` | Dockerfiles for exercising a clean install. |

Docs
----

- [Carapace](docs/Carapace.md) — the system as a whole
- [Bundle](docs/Bundle.md) — how bundles work
- [Module](docs/Module.md) — how to write a module
- [Host](docs/Host.md) / [Host Config](docs/Host-Config.md) — per-host overrides
- [TODO](docs/TODO.md) — known gaps
