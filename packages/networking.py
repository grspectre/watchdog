# -*- coding: utf8 -*-

import SocketServer
import threading
import socket
import threading
import random
import hashlib
import time


class WatchdogThreadingSocketServer(SocketServer.ThreadingTCPServer):
    __in_queue = None
    __out_queue = None
    queued_data = {}

    def set_in_queue(self, queue):
        self.__in_queue = queue

    def set_out_queue(self, queue):
        self.__out_queue = queue

    def handle_queue(self):
        for unique_id in self.queued_data:
            item = self.queued_data[unique_id]
            if item["type"] == "out" and item["data"] is not None:
                self.__out_queue.put({
                    "id": unique_id,
                    "data": item["data"]
                })
                self.queued_data[unique_id]["type"] = "in"
                self.queued_data[unique_id]["data"] = None

        while not self.__in_queue.empty():
            item = self.__in_queue.get()
            if item["id"] in self.queued_data:
                self.queued_data[item["id"]]["data"] = item["data"]

    def process_request(self, request, client_address):
        """Start a new thread to process the request."""
        self.handle_queue()
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
        self.server.queued_data[self.__unique_id] = {
            "type": "out",
            "data": None
        }

    def handle(self):
        data = self.request.recv(65535)
        self.server.queued_data[self.__unique_id]["data"] = data
        check_data = True
        while check_data:
            time.sleep(0.5)
            item = self.server.queued_data[self.__unique_id]
            if item["type"] == "in" and item["data"] is not None:
                check_data = False
                response = item["data"]
        self.request.sendall(response)

    def finish(self):
        del(self.server.data_from_request[self.__unique_id])


class WatchdogTCPClient:

    def __init__(self):
        pass
