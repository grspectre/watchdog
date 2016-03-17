# -*- coding: utf8
from packages.configuration import Configuration


class BasePlugin:
    __bi_queue = None

    def __init__(self, bi_queue, config_path):
        """
        Constructor
        :type bi_queue: packages.bidirectional_queue.BidirectionalQueue
        :type config_path: str
        :return:
        """
        self.__bi_queue = bi_queue

    def handle(self, params):
        """
        Serve
        :type params: dict
        :return:
        """
        pass
