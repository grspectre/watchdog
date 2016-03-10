# -*- coding: utf8 -*-

import SocketServer
import threading
import socket
import threading
import random
import hashlib
import time


class WatchdogThreadingSocketServer(SocketServer.ThreadingTCPServer):
    __queue = None
    data_from_request = {}

    def set_in_queue(self, queue):
        self.__queue = queue

    def process_request(self, request, client_address):
        """Start a new thread to process the request."""
        t = threading.Thread(target = self.process_request_thread,
                             args = (request, client_address))
        t.daemon = self.daemon_threads
        t.start()


class WatchdogTCPRequestHandler(SocketServer.BaseRequestHandler):

    __unique_id = None

    def setup(self):
        unique_str = str(time.time())+str(random.random())
        md5_hash = hashlib.md5(unique_str)
        self.__unique_id = md5_hash.hexdigits()
        self.server.data_from_request[self.__unique_id] = {
            "data_from_request_sended": False,
            "data_from_request": None,
            "data_from_worker_received": False,
            "data_from_worker": None
        }

    def handle(self):
        print self.server.get_queue()
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
        self.request.sendall(response)

    def finish(self):
        del(self.server.data_from_request[self.__unique_id])


class WatchdogTCPClient:

    def __init__(self):
        pass
