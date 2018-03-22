# -*- coding: utf-8 -*-
"""
    Get battery.
"""

import subprocess
import re

ANSI_ESCAPE = re.compile(r'\x1b[^m]*m')
FULL_CHARS = set(['#'])
EMPTY_CHARS = set(['.', '!', '+'])

class Py3status:
    format = "B: {bar} {percent}% ({time})"
    cache = 30
    low = 20
    mid = 40
    fine = 95
    color_low  = "#FF0000" # bold red
    color_mid  = "#CD0000" # nobold red
    color_fine = "#00CD00" # nobold green
    color_full = "#00FF00" # bold green

    def ibam_battery_prompt(self):
        cmd = self.py3.check_commands(["ibam-battery-prompt"])
        output = subprocess.check_output([cmd, '-p'], stderr=None)
        lines = [ANSI_ESCAPE.sub('', x.strip()) for x in output.strip().split('\n')]

        parts = {
            'bar': "",
            'time': "",
            'charging': False,
            'percent_tens': 0,
            'percent': 0,
        }

        if (len(lines) > 0):
            parts['bar'] = lines[0]
        if (len(lines) > 1):
            parts['time'] = lines[1]
        if (len(lines) > 2):
            parts['charging'] = (lines[2] == "True")
        if (len(lines) > 3):
            try:
                parts['percent_tens'] = int(lines[3])
            except ValueError:
                parts['percent_tens'] = 0
        if (len(lines) > 4):
            try:
                parts['percent'] = int(lines[4])
            except ValueError:
                parts['percent'] = 0
        if (parts['percent'] < self.low):
            color = self.color_low
        elif (parts['percent'] < self.mid):
            color = self.color_mid
        elif (parts['percent'] < self.fine):
            color = self.color_fine
        else:
            color = self.color_full

        return {
            'full_text': self.py3.safe_format(self.format, parts),
            'cached_until': self.py3.time_in(self.cache),
            'color': color,
        }
