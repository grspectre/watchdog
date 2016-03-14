# -*- coding: utf8 -*-
from types import *
import fnmatch

class Wildcard:
    """Wildcard class"""
    __wildcards = []

    def __init__(self, wildcards):
        """
        Constructor
        :type self: packages.wildcard.Wildcard
        :type wildcards: list
        """
        self.set(wildcards)

    def add(self, wildcard):
        """
        Add wildcard to array for checking
        :type self: packages.wildcard.Wildcard
        :type wildcard: str
        :return: void
        :raise RuntimeError
        """
        if type(wildcard) is not StringType:
            raise RuntimeError('Wildcard is not a string')
        self.__wildcards.append(wildcard)

    def set(self, wildcards):
        """
        Set wildcards to array for checking
        :type self: packages.wildcard.Wildcard
        :type wildcards: list
        :return: void
        :raise: RuntimeError
        """
        cleared_wildcards = []
        if type(wildcards) is not ListType:
            raise RuntimeError('Wildcards is not a list')
        for wildcard in wildcards:
            if type(wildcard) is not StringType:
                raise RuntimeError('Wildcard is not a string')
            cleared_wildcards.append(wildcard)
        self.__wildcards = cleared_wildcards

    def clear(self):
        """
        Clear wildcards array
        :type self: packages.wildcard.Wildcard
        :return: void
        """
        self.__wildcards = []

    def check(self, checking_string):
        """
        Check checking_string
        :type self: packages.wildcard.Wildcard
        :param checking_string:
        :return:
        """
        if len(self.__wildcards) == 0:
            return False
        for wildcard in self.__wildcards:
            if fnmatch.fnmatchcase(checking_string, wildcard):
                return True
        return False
