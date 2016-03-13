#!/usr/bin/env python
# -*- coding: utf8 -*-

from multiprocessing import Queue, Process
from packages.configuration import Configuration
from packages.networking import WatchdogTCPRequestHandler, WatchdogThreadingSocketServer, handle_queue
from packages.queue_pool import QueuePool
import os
import threading
import time


def init_server(configuration, queue_pool):
    """
    Initiate a socket server
    :type configuration: packages.configuration.Configuration
    :type queue_pool: packages.queue_pool.QueuePool
    :return:
    """
    host = configuration.get("server::host")
    port = configuration.get("server::port")
    server = WatchdogThreadingSocketServer((host, port), WatchdogTCPRequestHandler)
    handle_queue_thread = threading.Thread(target = handle_queue,
                         args = (server, queue_pool))
    handle_queue_thread.start()
    server.serve_forever()

def init_worker(server_queue, worker_queue):
    """
    :param queue:
    :return:
    """
    while True:
        pass


def serve(configuration, queue_pool):
    while True:
        items = queue_pool.getAll('parent')
        for item in items:
            queue_pool.put('parent', item)
        # TODO: Magic number!
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
    srv_queue_pool = QueuePool(in_server_queue, out_server_queue)
    server_process = Process(target=init_server, args=(configuration, srv_queue_pool))
    server_process.start()
    serve(configuration, srv_queue_pool)



if __name__=="__main__":
    init()