#!/usr/bin/env python
# -*- coding: utf8 -*-

from multiprocessing import Queue, Process
from packages.configuration import Configuration
from packages.networking import WatchdogTCPRequestHandler, WatchdogThreadingSocketServer, handle_queue
from packages.bidirectional_queue import BidirectionalQueue
import os
import threading
import time


def init_server(configuration, bi_queue):
    """
    Initiate a socket server
    :type configuration: packages.configuration.Configuration
    :type queue_pool: packages.queue_pool.QueuePool
    :return:
    """
    host = configuration.get("server::host")
    port = configuration.get("server::port")
    server = WatchdogThreadingSocketServer((host, port), WatchdogTCPRequestHandler)
    handle_queue_thread = threading.Thread(target=handle_queue, args=(server, bi_queue))
    handle_queue_thread.start()
    server.serve_forever()


def init_worker(configuration_path, bi_queue):
    """
    :type configuration_path: str
    :type bi_queue: packages.bidirectional_queue.BidirectionalQueue
    :return:
    """
    while True:
        pass


def serve(configuration, bi_queue):
    while True:
        items = bi_queue.get_all('parent')
        for item in items:
            bi_queue.put('parent', item)
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
    srv_bi_queue = BidirectionalQueue(Queue(), Queue())
    server_process = Process(target=init_server, args=(configuration, srv_bi_queue))
    server_process.start()
    serve(configuration, srv_bi_queue)


if __name__ == "__main__":
    init()
