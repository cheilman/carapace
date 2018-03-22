# -*- coding: utf-8 -*-
"""
    Run a command and display based on exit code.
"""

import subprocess
import re

class Py3status:
    format = "K"
    cache = 30
    color_pass = "#00FF00"
    color_fail = "#FF0000"

    def kerberos(self):
        cmd = self.py3.check_commands(["klist"])
        exitcode = subprocess.call([cmd, '-s'])

        parts = {'code': -1}

        parts['code'] = exitcode

        color = self.color_fail
        if exitcode == 0:
            color = self.color_pass

        return {
            'full_text': self.py3.safe_format(self.format, parts),
            'cached_until': self.py3.time_in(self.cache),
            'color': color,
        }


