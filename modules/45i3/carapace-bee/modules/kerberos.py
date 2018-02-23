# pylint: disable=C0111,R0903

"""See what the current state of my kerberos ticket is.

Requires the following executable:
    * klist

Parameters:
    kerberos.frequency      How often to check (in seconds)
"""

import re
import time
import threading

import bumblebee.input
import bumblebee.output
import bumblebee.engine

def has_ticket(module, widget):
    try:
        res = bumblebee.util.execute("klist -s")
        widget.set("krb-ticket", True)
    except Exception as e:
        widget.set("krb-ticket", False)

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text="K")
        super(Module, self).__init__(engine, config, widget)

        widget.set("krb-frequency", self.parameter("frequency", 10))
        widget.set("krb-ticket", False)

        self._next_check = 0

    def state(self, widget):
        if not widget.get("krb-ticket"): return ["critical"]
        return None

    def update(self, widgets):
        if int(time.time()) < self._next_check:
            return
        thread = threading.Thread(target=has_ticket, args=(self, widgets[0],))
        thread.start()
        self._next_check = int(time.time()) + int(widgets[0].get("krb-frequency"))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
