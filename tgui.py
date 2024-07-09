"""Base module.
"""

import curses
from curses import wrapper


class TGUI:
    """Base class.
    """

    def __init__(self, a_dict={}):
        """Initialize self. See help(type(self)) for accurate signature.
        """

        self._kwargs = a_dict

    def main(self, window):
        """Callback method for curses.wrapper function, called before the run
        method.
        Serves as the entry point for a user program.

        Args:
            window (obj): curses window object representing the default screen
                          created by curses.initscr().
        """

        self._win = window

        # set screen properties
        curses.curs_set(0)

        # other curses inits goes here...

        self._win.getch()

    def run(self):
        curses.wrapper(self.main)
