"""Base module.
"""

import curses
from curses import wrapper


class TGUI:
    """Base class.
    """

    def __init__(self):
        """Initialize self. See help(type(self)) for accurate signature.
        """

    def tgui(self, stdscr):
        """Callback method for curses.wrapper function, called before the run
        method.

        Args:
            stdscr (obj): curses window object representing the default screen
                          created by curses.initscr().

        Return:
            return stdscr
        """

        # set screen properties
        curses.curs_set(0)

        # other inits goes here...

        return stdscr

    def run(self):
        curses.wrapper(self.tgui)
