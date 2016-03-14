# -*- coding: utf8 -*-


class BidirectionalQueue:
    __in_queue = None
    __out_queue = None

    def __init__(self, in_queue, out_queue, who_create = 'parent'):
        """
        Constuctor
        :type in_queue: multiprocessing.Queue
        :type out_queue: multiprocessing.Queue
        :type who_create: parent|child
        :return:
        """
        self.__check('who_create', who_create)
        if who_create == 'parent':
            self.__in_queue = in_queue
            self.__out_queue = out_queue
        if who_create == 'child':
            self.__in_queue = out_queue
            self.__out_queue = in_queue

    def put(self, who_am_i, value):
        """
        Put value to queue
        :type who_am_i: str
        :type value: dict
        :return:
        """
        self.__check('who_am_i', who_am_i)
        if who_am_i == 'parent':
            self.__out_queue.put(value)
        if who_am_i == 'child':
            self.__in_queue.put(value)

    def get(self, who_am_i):
        """
        Get value from queue
        :type who_am_i: str
        :return:
        """
        self.__check('who_am_i', who_am_i)
        if who_am_i == 'parent':
            if not self.__in_queue.empty():
                return self.__in_queue.get()
            else:
                return None
        if who_am_i == 'child':
            if not self.__out_queue.empty():
                return self.__out_queue.get()
            else:
                return None

    def getAll(self, who_am_i):
        """
        Get all values from Queue
        :type who_am_i: str
        :return: list
        """
        self.__check('who_am_i', who_am_i)
        result = []
        if who_am_i == 'parent':
            while not self.__in_queue.empty():
                result.append(self.__in_queue.get())
        if who_am_i == 'child':
            while not self.__out_queue.empty():
                result.append(self.__out_queue.get())
        return result

    def __check(self, name_param, value):
        if value != 'parent' and value != 'child':
            raise RuntimeError("Parameter %s not equals 'parent' or 'child'" % (name_param,))
