#!/usr/bin/env python
# -*- coding: utf8 -*-

from multiprocessing import Queue, Process
from packages.configuration import Configuration
from packages.networking import WatchdogTCPRequestHandler, WatchdogThreadingSocketServer
import os


def init_server(configuration, queue):
    """
    Initiate a socket server
    :type configuration: packages.configuration.Configuration
    :return:
    """
    host = configuration.get("server::host")
    port = configuration.get("server::port")
    server = WatchdogThreadingSocketServer((host, port), WatchdogTCPRequestHandler)
    server.set_queue(queue)
    server.serve_forever()

def init_worker(server_queue, ):
    """
    :param queue:
    :return:
    """
    while True:
        pass


def init():
    """
    Init watchdog server
    :return:
    """
    configuration_path = os.path.join(os.path.dirname(__file__), 'config')
    configuration_name = 'watchdog'
    configuration = Configuration(configuration_path, configuration_name)
    server_queue = Queue()
    server_process = Process(target=init_server, args=(configuration, server_queue))
    server_process.start()



if __name__=="__main__":
    init()