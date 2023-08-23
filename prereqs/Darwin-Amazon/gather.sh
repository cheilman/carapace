#!/bin/bash
#
# Gather installed information
#

brew list --cask | sort > brew-casks

brew list --formulae -tr -1 | sort > brew-formulae

brew leaves --installed-on-request | sort > brew-leaves-installed-on-request
brew leaves --installed-on-request | sort | xargs brew desc --eval-all > brew-leaves-installed-on-request-with-desc


