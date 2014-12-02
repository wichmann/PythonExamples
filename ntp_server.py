#!/usr/bin/env python3

"""
Zeit von NTP-Server abfragen

@author: Christian Wichmann
@license: GNU GPL
"""

import ntplib
from time import ctime


def call_time_server():
    c = ntplib.NTPClient()
    response = c.request('pool.ntp.org')
    print(ctime(response.tx_time))


if __name__ == '__main__':
    call_time_server()
