# -*- coding: utf8 -*-
import json
import os


class Configuration:
    """Configuration class"""
    __configuration = None

    def __init__(self, path, name):
        """
        Constructor
        :type self: packages.configuration.Configuration
        :type path: str
        :type name: str
        :raise RuntimeError
        :return void
        """
        filename = os.path.join(path, name+'.json')
        if os.path.isfile(filename):
            config = open(filename, 'rb').read()
        else:
            raise RuntimeError("Configuration file does not exists")
        try:
            self.__configuration = json.loads(config)
        except ValueError:
            raise RuntimeError("Can not decode JSON files")

    def get(self, key):
        """
        Get configuration parameter by key separated with ::
        :type self: packages.configuration.Configuration
        :type key: str
        :return mixed
        """
        split_key = key.split('::')
        temp_value = self.__configuration
        for one_key in split_key:
            try:
                temp_value = temp_value[one_key]
            except KeyError:
                return None
        return temp_value
