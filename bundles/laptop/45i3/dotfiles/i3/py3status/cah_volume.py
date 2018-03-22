# -*- coding: utf-8 -*-
"""
    Get volume.
"""

import subprocess
import re

ANSI_ESCAPE = re.compile(r'\x1b[^m]*m')
SINK_LINE = re.compile(r'^(?P<index>[0-9]+): (?P<name>.*) (?P<volume>[0-9]+)% \((?P<muted>.*)\)$')

class Py3status:
    format = "\u1F3B5: {volume}% ({muted})"
    cache = 30
    color_mute = "#FF0000"
    color_unmute = "#00FF00"

    def cah_volume(self):
        parts = {
            'index': "",
            'name': "",
            'volume': "",
            'muted': "",
        }
        color = "#FFFFFF"

        try:
            cmd = self.py3.check_commands(["audio-status"])
            output = subprocess.check_output([cmd, '-d'], stderr=None)
            lines = [ANSI_ESCAPE.sub('', x.strip()) for x in output.strip().split('\n')]

            # Just look at first line (there should only be one)
            m =  SINK_LINE.match(lines[0])

            if m:
                parts['index'] = m.group('index')
                parts['name'] = m.group('name')
                parts['volume'] = m.group('volume')
                parts['muted'] = m.group('muted')

                if parts['muted'] == 'muted':
                    color = self.color_mute
                else:
                    color = self.color_unmute
        except subprocess.CalledProcessError:
            pass

        return {
            'full_text': self.py3.safe_format(self.format, parts),
            'cached_until': self.py3.time_in(self.cache),
            'color': color,
        }
