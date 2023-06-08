#!bash
#
# Writes brew installed packages to a bunch of files
#

brew list --cask | sort > brew-casks
brew list --formulae -tr -1 | sort > brew-formulae
brew leaves --installed-on-request | sort > brew-leaves-installed-on-request
brew leaves --installed-on-request | xargs brew desc --eval-all | sort > brew-leaves-installed-on-request-with-desc

