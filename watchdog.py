#!/usr/bin/env python
# -*- coding: utf8 -*-

from packages.configuration import Configuration
from packages.networking import WatchdogTCPRequestHandler, WatchdogThreadingSocketServer, handle_queue
from packages.bidirectional_queue import BidirectionalQueue
from packages.tools import CheckInterval
from multiprocessing import Queue, Process, cpu_count
import os
import threading
import time


def get_plugins_config():
    pass


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


def handle_worker(configuration_path, bi_queue):
    """
    :type configuration_path: str
    :type bi_queue: packages.bidirectional_queue.BidirectionalQueue
    :return:
    """
    while True:
        # TODO: Magic number!
        time.sleep(0.1)


def serve(configuration, srv_bi_queue, wrk_bi_queue):
    check_interval = CheckInterval()
    check_interval.add_interval(15)
    check_interval.add_interval(30)
    while True:
        items = srv_bi_queue.get_all('parent')
        for item in items:
            srv_bi_queue.put('parent', item)
        current_intervals = check_interval.fire()
        if len(current_intervals) > 0:
            print current_intervals
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

    process_count = configuration.get("process_count")
    process_count = int(process_count)
    # TODO: Magic number!
    if process_count > 8:
        process_count = 8
    if process_count == 0:
        process_count = cpu_count()

    wrk_bi_queue = BidirectionalQueue(Queue(), Queue())
    for count in range(process_count):
        wrk_process = Process(target=handle_worker, args=(configuration, wrk_bi_queue))
        wrk_process.start()

    serve(configuration, srv_bi_queue, wrk_bi_queue)


if __name__ == "__main__":
    init()
