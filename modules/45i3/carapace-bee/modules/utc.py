# pylint: disable=C0111,R0903

"""Displays the current date and time, from UTC (or other) time zone.

Parameters:
    * utc.format: strftime()-compatible formatting string
    * utc.locale: locale to use rather than the system default
"""

from __future__ import absolute_import
import datetime
import locale
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.get_time))
        self._fmt = self.parameter("format", "%H:%M")
        l = locale.getdefaultlocale()
        if not l:
            l = ('en_US', 'UTF-8')
        lcl = self.parameter("locale", ".".join(l))
        locale.setlocale(locale.LC_TIME, lcl.split("."))

    def get_time(self, widget):
        enc = locale.getpreferredencoding()
        retval = datetime.datetime.utcnow().strftime(self._fmt)
        if hasattr(retval, "decode"):
            return retval.decode(enc)
        return retval

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
