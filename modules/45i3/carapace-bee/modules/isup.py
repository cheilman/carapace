# pylint: disable=C0111,R0903

"""Attempts to hit a site, errors if failure.

Requires the following executable:
    * ping

Parameters:
    * isup.interval: Time in seconds between two isup checks (defaults to 60)
    * isup.address : IP address to check
    * isup.timeout : Timeout for waiting for a reply (defaults to 5.0)
    * isup.probes  : Number of probes to send (defaults to 5)
    * isup.warning : Threshold for warning state, in seconds (defaults to 1.0)
    * isup.critical: Threshold for critical state, in seconds (defaults to 2.0)
"""

import re
import time
import threading

import bumblebee.input
import bumblebee.output
import bumblebee.engine

def get_isup(module, widget):
    try:
        res = bumblebee.util.execute("ping -n -q -c 1 -W {} {}".format(
            widget.get("isup-timeout"), widget.get("address")
        ))
        widget.set("isup-unreachable", False)
        widget.set("isup-downcount", 0)
    except Exception as e:
        widget.set("isup-unreachable", True)
        widget.set("isup-downcount", widget.get("isup-downcount", 0))

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.isup)
        super(Module, self).__init__(engine, config, widget)

        addr=self.parameter("address", "8.8.8.8")

        widget.set("address", addr)
        widget.set("name", self.parameter("name", addr))
        widget.set("interval", self.parameter("interval", 30))
        widget.set("isup-timeout", self.parameter("timeout", 5.0))
        widget.set("isup-unreachable", False)
        widget.set("isup-downcount", 0)

        self._next_check = 0

    def isup(self, widget):
        return widget.get("name")

    def state(self, widget):
        if widget.get("isup-unreachable"): return ["critical"]
        return None

    def update(self, widgets):
        if int(time.time()) < self._next_check:
            return
        thread = threading.Thread(target=get_isup, args=(self, widgets[0],))
        thread.start()
        self._next_check = int(time.time()) + int(widgets[0].get("interval"))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
