# -*- coding: utf8 -*-


class Wildcard:
    """Wildcard class"""
    __wildcards = []

    def __init__(self):
        """
        Constructor
        """
        pass

    def add(self, wildcard):
        """
        Add wildcard to array for checking
        :type self: packages.wildcard.Wildcard
        :type wildcard: str
        :return: void
        :raise RuntimeError
        """
        pass

    def set(self, wildcards):
        """
        Set wildcards to array for checking
        :type self: packages.wildcard.Wildcard
        :type wildcards: list
        :return: void
        :raise: RuntimeError
        """
        pass

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
        pass

    def __prepare(self, wildcard):
        pass