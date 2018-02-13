# -*- coding: utf-8 -*-
"""
    Run a command and display based on exit code.
"""

import subprocess
import re

class Py3status:
    format = "Y"
    cache = 30
    color_pass = "#FF00FF"
    color_fail = "#00FFFF"

    def kerberos(self):

        task = subprocess.Popen('xinput list-props "Yubico Yubikey 4 OTP+U2F" | grep  "Device Enabled" | cut -d\: -f 2 | sed -e "s/[ \t]*//g"', shell=True, stdout=subprocess.PIPE)
        task.wait()
        data = task.stdout.read()

        try:
            value = int(data)
        except Exception:
            value = -1

        parts = {'value': value}

        color = self.color_fail
        if value == 1:
            color = self.color_pass

        return {
            'full_text': self.py3.safe_format(self.format, parts),
            'cached_until': self.py3.time_in(self.cache),
            'color': color,
        }


