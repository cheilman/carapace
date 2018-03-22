# pylint: disable=C0111,R0903

"""See what the current state of my yubikey-as-keyboard is.

Requires the following executable:
    * xinput

Parameters:
    yubikey.frequency   How often to check (in seconds)
"""

import re
import time
import threading

import bumblebee.input
import bumblebee.output
import bumblebee.engine

def y_enabled(module, widget):
    try:
        res = bumblebee.util.execute('/usr/bin/xinput list-props "Yubico Yubikey 4 OTP+U2F"')

        for line in res.split('\n'):
            if "Device Enabled" in line:
                val = int(line.split(":")[1])

                if val == 1:
                    widget.set("yubi-enabled", True)
                    return

        widget.set("yubi-enabled", False)
    except Exception as e:
        print e
        widget.set("yubi-enabled", False)

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text="Y")
        super(Module, self).__init__(engine, config, widget)

        widget.set("yubi-frequency", self.parameter("frequency", 5))
        widget.set("yubi-enabled", False)

        self._next_check = 0

    def state(self, widget):
        if widget.get("yubi-enabled"): return ["critical"]
        return None

    def update(self, widgets):
        if int(time.time()) < self._next_check:
            return
        thread = threading.Thread(target=y_enabled, args=(self, widgets[0],))
        thread.start()
        self._next_check = int(time.time()) + int(widgets[0].get("yubi-frequency"))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
