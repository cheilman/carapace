#!/usr/bin/env python3
#
# Pretty the hostname up
#

import socket
import subprocess

def prettyhostname(pl):
    try:
        hn = subprocess.check_output(['pretty-hostname'])
    except:
        hn = socket.gethostname()

    if hn:
        hn = hn.strip()

    return [{
        'contents': hn,
        'highlight_groups': ['hostname']
    }]

if __name__ == "__main__":
    print(prettyhostname())

