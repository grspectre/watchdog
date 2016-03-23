#!/usr/bin/env python
# -*- coding: utf8 -*-

from packages.configuration import Configuration
from packages.networking import WatchdogTCPRequestHandler, WatchdogThreadingSocketServer, handle_queue
from packages.bidirectional_queue import BidirectionalQueue
from packages.tools import CheckInterval
from packages.wildcard import Wildcard
from multiprocessing import Queue, Process, cpu_count
import os
import threading
import time


def get_plugins_config(configuration_path):
    """
    Get plugins config from all plugins config files
    :type configuration_path: str
    :return:
    """
    result = {}
    wildcard = Wildcard(["*.json"])
    files = os.listdir(configuration_path)
    for name in files:
        if not wildcard.check(name):
            continue
        name_without_ext = name.replace(".json", "")
        config = Configuration(configuration_path, name_without_ext)
        result[name_without_ext] = {
            "name": config.get("name"),
            "public_methods": config.get("public_methods"),
            "interval": config.get("interval"),
            "enable": config.get("enable")
        }
    return result


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
    plugins = get_plugins_config(configuration_path)
    while True:
        # TODO: Magic number!
        time.sleep(0.1)


def serve(configuration_path, srv_bi_queue, wrk_bi_queue):
    plugins_configuration_path = os.path.join(configuration_path, 'plugins')
    plugins = get_plugins_config(plugins_configuration_path)
    while True:
        items = srv_bi_queue.get_all('parent')
        for item in items:
            srv_bi_queue.put('parent', item)
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
    plugins_configuration_path = os.path.join(configuration_path, "plugins")
    for count in range(process_count):
        wrk_process = Process(target=handle_worker, args=(plugins_configuration_path, wrk_bi_queue))
        wrk_process.start()

    serve(configuration_path, srv_bi_queue, wrk_bi_queue)


if __name__ == "__main__":
    init()
