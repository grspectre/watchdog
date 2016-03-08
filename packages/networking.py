# -*- coding: utf8 -*-

import SocketServer
import threading
import socket

class WatchdogThreadingSocketServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class WatchdogTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
        self.request.sendall(response)

class WatchdogTCPClient:
    pass