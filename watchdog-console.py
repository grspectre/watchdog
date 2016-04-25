#!/usr/bin/env python
# -*- coding: utf8 -*-

from packages.configuration import Configuration
import os
import socket


def init():
    """
    Init watchdog console
    :return:
    """
    configuration_path = os.path.join(os.path.dirname(__file__), 'config')
    configuration_name = 'watchdog'
    configuration = Configuration(configuration_path, configuration_name)
    host = configuration.get("console::host")
    port = configuration.get("console::port")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = "list"

    try:
        # Connect to server and send data
        sock.connect((host, port))
        sock.sendall(data + "\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
    finally:
        sock.close()
    print "Sent:     {}".format(data)
    print "Received: {}".format(received)

if __name__=='__main__':
    init()