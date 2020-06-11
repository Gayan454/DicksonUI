#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  utiles.py
#
#  Copyright 2020  <Kavindu Santhusa>
#

import socket


def find_free_port(_port, max_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while _port <= max_port:
        try:
            sock.bind(('', _port))
            s, port = sock.getsockname()
            sock.close()
            return port
        except:
            _port += 1
    raise IOError('no free ports')
