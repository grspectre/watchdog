#!/usr/bin/env python
# -*- coding: utf8 -*-

from packages.configuration import Configuration
from packages.networking import WatchdogTCPRequestHandler, WatchdogThreadingSocketServer, handle_queue
from packages.bidirectional_queue import BidirectionalQueue
from packages.tools import CheckInterval
from packages.wildcard import Wildcard
from multiprocessing import Queue, Process, Value, cpu_count
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
        config_keys = config.keys()
        result[name_without_ext] = {}
        for key in config_keys:
            result[name_without_ext][key] = config.get(key)

    return result


def init_plugins(configuration_path, work_path):
    plugins_config_data = get_plugins_config(configuration_path)
    print plugins_config_data
    return None


def init_server(configuration, bi_queue, serve_forever):
    """
    Initiate a socket server
    :type configuration: packages.configuration.Configuration
    :type bi_queue: packages.bidirectional_queue.BidirectionalQueue
    :type serve_forever: multiprocessing.Value
    :return:
    """
    host = configuration.get("server::host")
    port = configuration.get("server::port")
    server = WatchdogThreadingSocketServer((host, port), WatchdogTCPRequestHandler)
    handle_queue_thread = threading.Thread(target=handle_queue, args=(server, bi_queue, serve_forever))
    handle_queue_thread.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # shutdown server
        for unique_id in server.queued_data:
            server.queued_data[unique_id]["data"] = "stop server"
        server.shutdown()


def handle_worker(configuration_path, bi_queue, serve_forever):
    """
    :type configuration_path: str
    :type bi_queue: packages.bidirectional_queue.BidirectionalQueue
    :type serve_forever: multiprocessing.Value
    :return:
    """
    try:
        plugins = get_plugins_config(configuration_path)

        while serve_forever.value == 1:
            item = bi_queue.get('child')

            # TODO: Magic number!
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        pass


def serve(configuration, configuration_path, srv_bi_queue, wrk_bi_queue, serve_forever):

    plugins_configuration_path = os.path.join(configuration_path, 'plugins')

    result = init_plugins(plugins_configuration_path, configuration.get('work_path'))
    if result is None:
        serve_forever.value = 0

    try:
        while serve_forever.value == 1:
            items = srv_bi_queue.get_all('parent')
            for item in items:
                srv_bi_queue.put('parent', item)
            # TODO: Magic number!
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        pass



def init():
    """
    Init watchdog server
    :return:
    """
    configuration_path = os.path.join(os.path.dirname(__file__), 'config')
    configuration_name = 'watchdog'
    configuration = Configuration(configuration_path, configuration_name)

    serve_forever = Value('i', 1)

    srv_bi_queue = BidirectionalQueue(Queue(), Queue())
    server_process = Process(target=init_server, args=(configuration, srv_bi_queue, serve_forever))
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
    wrk_processes = []
    for count in range(process_count):
        wrk_process = Process(target=handle_worker, args=(plugins_configuration_path, wrk_bi_queue, serve_forever))
        wrk_process.start()

    serve(configuration, configuration_path, srv_bi_queue, wrk_bi_queue, serve_forever)

    # shutdown
    server_process.join()
    for process in wrk_processes:
        process.join()

if __name__ == "__main__":
    init()
