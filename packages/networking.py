# -*- coding: utf8 -*-

import SocketServer
import threading
import socket


class WatchdogThreadingSocketServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    __queue = None

    def set_queue(self, queue):
        self.__queue = queue

    def get_queue(self):
        return self.__queue


class WatchdogTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        print self.server.get_queue()
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
        self.request.sendall(response)


class WatchdogTCPClient:

    def __init__(self):
        pass
