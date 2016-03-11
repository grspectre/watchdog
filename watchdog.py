#!/usr/bin/env python
# -*- coding: utf8 -*-

from multiprocessing import Queue, Process
from packages.configuration import Configuration
from packages.networking import WatchdogTCPRequestHandler, WatchdogThreadingSocketServer, handle_queue
import os
import threading
import time


def init_server(configuration, in_queue, out_queue):
    """
    Initiate a socket server
    :type configuration: packages.configuration.Configuration
    :return:
    """
    host = configuration.get("server::host")
    port = configuration.get("server::port")
    server = WatchdogThreadingSocketServer((host, port), WatchdogTCPRequestHandler)
    handle_queue_thread = threading.Thread(target = handle_queue,
                         args = (server, out_queue, in_queue))
    handle_queue_thread.start()
    server.serve_forever()

def init_worker(server_queue, worker_queue):
    """
    :param queue:
    :return:
    """
    while True:
        pass


def serve(configuration, in_server_queue, out_server_queue):
    while True:
        while not in_server_queue.empty():
            data = in_server_queue.get()
            out_server_queue.put(data)
        time.sleep(0.1)


def init():
    """
    Init watchdog server
    :return:
    """
    configuration_path = os.path.join(os.path.dirname(__file__), 'config')
    configuration_name = 'watchdog'
    configuration = Configuration(configuration_path, configuration_name)
    in_server_queue = Queue()
    out_server_queue = Queue()
    server_process = Process(target=init_server, args=(configuration, in_server_queue, out_server_queue))
    server_process.start()
    serve(configuration, in_server_queue, out_server_queue)



if __name__=="__main__":
    init()