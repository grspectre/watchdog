# -*- coding: utf8 -*-

import SocketServer
import threading
import socket
import threading
import random
import hashlib
import time


def handle_queue(server, bi_queue):
    while True:
        for unique_id in server.queued_data:
            item = server.queued_data[unique_id]
            if item["type"] == "out" and item["data"] is not None:
                bi_queue.put('child', {
                    "id": unique_id,
                    "data": item["data"]
                })
                server.queued_data[unique_id]["type"] = "in"
                server.queued_data[unique_id]["data"] = None

        items = bi_queue.get_all('child')
        for item in items:
            if item["id"] in server.queued_data:
                server.queued_data[item["id"]]["data"] = item["data"]

        # TODO: Magic number!
        time.sleep(0.1)


class WatchdogThreadingSocketServer(SocketServer.ThreadingTCPServer):
    queued_data = {}


class WatchdogTCPRequestHandler(SocketServer.BaseRequestHandler):

    __unique_id = None

    def setup(self):
        unique_str = str(time.time())+str(random.random())
        md5_hash = hashlib.md5(unique_str)
        self.__unique_id = md5_hash.hexdigest()
        self.server.queued_data[self.__unique_id] = {
            "type": "out",
            "data": None
        }

    def handle(self):
        # TODO: Magic number!
        data = self.request.recv(65535)
        self.server.queued_data[self.__unique_id]["data"] = data
        check_data = True
        response = ''
        while check_data:
            # TODO: Magic number!
            time.sleep(0.1)
            item = self.server.queued_data[self.__unique_id]
            if item["type"] == "in" and item["data"] is not None:
                check_data = False
                response = item["data"]
        self.request.sendall(response)

    def finish(self):
        del(self.server.queued_data[self.__unique_id])


class WatchdogTCPClient:

    def __init__(self):
        pass
