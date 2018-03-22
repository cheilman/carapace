Carapace Bundles
================

What makes up a bundle?
-----------------------

A bundle is simply a grouped collection of modules.

Bundle Structure
----------------

```
mybundle/
 |- 10mod1
 |- 20mod2
 |- 30mod3
 ...
```

At this time, there is no special inclusion logic or anything.  The idea is that bundles can be separate repositories and cloned into the systems that matter.

What does the module installation process look like?
----------------------------------------------------

1. Loop through each bundle in shell order
2. Check if there are any modules that are linked into this bundle that no longer exist, if so remove them
3. Link all modules from this bundle into the module root

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
