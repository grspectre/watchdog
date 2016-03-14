#! -*- coding: utf8 -*-
import time
import math


class CheckInterval:
    """
    CheckInterval class
    """
    __begin_time = None
    __intervals = {}

    def __init__(self):
        """
        Constructor
        :return:
        """
        self.__begin_time = time.mktime(time.gmtime())

    def add_interval(self, interval):
        """
        Add interval to list
        :type interval: int
        :return:
        """
        interval = int(interval)
        if interval == 0:
            return
        self.__intervals[str(interval)] = 0

    def fire(self):
        """
        Return fired intervals
        :return: list
        """
        result = []
        current_time = time.mktime(time.gmtime())
        seconds_from_begin = current_time - self.__begin_time
        for interval in self.__intervals:
            int_interval = int(interval)
            how_many_times = int(math.floor(seconds_from_begin/int_interval))
            if self.__intervals[interval] != how_many_times:
                self.__intervals[interval] = how_many_times
                result.append(int_interval)
        return result