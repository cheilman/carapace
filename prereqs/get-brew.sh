#!bash
#
# Writes brew installed packages to a bunch of files
#

brew list --cask > brew-casks
brew list --formulae -tr -1 > brew-formulae
brew leaves --installed-on-request > brew-leaves-installed-on-request
brew leaves --installed-on-request | xargs brew desc --eval-all > brew-leaves-installed-on-request-with-desc

