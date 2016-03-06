# -*- coding: utf8 -*-
import json
import os

class Configuration:
    """Configuration class"""
    __configuration = None

    def __init__(self, path, name):
        """Constructor"""
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
        """Method Get"""
        splitKey = key.split('::')
        tempValue = self.__configuration
        for oneKey in splitKey:
            try:
                tempValue = tempValue[oneKey]
            except KeyError:
                return None
        return tempValue
