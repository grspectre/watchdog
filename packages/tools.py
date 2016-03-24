#! -*- coding: utf8 -*-
from packages.wildcard import Wildcard
from packages.configuration import Configuration
import time
import math
import os


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
    """
    Init plugins workaround
    :type configuration_path: str
    :type work_path: str
    :return:
    """
    plugins_config_data = get_plugins_config(configuration_path)
    for plugin in plugins_config_data:
        conf = plugins_config_data[plugin]
    return None


def prepare_work_path(work_path):
    abs_path = os.path.abspath(work_path)
    if os.path.isdir(abs_path):
        return abs_path
    else:
        raise RuntimeError("Work directory is not exists")