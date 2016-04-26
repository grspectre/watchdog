# -*- coding: utf8


class Interpreter:
    """
    Command interpreter class
    """
    plugins_configuration = None
    internal_commands = ['list', 'help']

    def __init__(self, plugins_conf):
        """
        Init method
        :type plugins_conf: list
        """
        self.plugins_configuration = plugins_conf

    def process(self, command_line):
        """
        Process command line
        :type command_line: str
        """
        print command_line
