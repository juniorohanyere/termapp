"""Base module for terminal GUI.
"""

import curses
from curses import wrapper


class TGUI:
    """Base class for Terminal GUI.
    """

    def __init__(self, a_dict={}):
        """Initialize self. See help(type(self)) for accurate signature.
        """

        self._kwargs = a_dict
        self._unblock = False

    def __app__(self, arg):
        """Callback method for a wrapper function (currently curses') called by
        the run method.
        Serves as the entry point for a user program.

        Args:
            arg: first and only parameter to be used by a wrapper
            function.
        """

        self._stdscr = arg

        # set screen properties
        curses.curs_set(0)

        # other curses inits goes here...

    def run(self):
        """Run the terminal GUI application.
        """

        curses.wrapper(self.__app__)
        if not self._unblock:
            self._stdscr.getch()
