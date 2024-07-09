"""Base module for terminal GUI.
"""

import curses


class TGUI:
    """Base class for Terminal GUI.
    """

    def __init__(self):
        """Initialize self. See help(type(self)) for accurate signature.
        """

        self._unblock = False
        self._stdscr = None

        self._color_pairs = {}

    def __app__(self, arg):
        """Callback method for a wrapper function (curses') called by
        the run method.
        Serves as the entry point for a user program for Terminal GUI.

        Args:
            arg: first and only parameter to be used by the wrapper function.
        """

        self._stdscr = arg

        # set screen properties
        curses.curs_set(0)

        # initilize color pairs
        self._color_pairs = self._set_color_pairs()

        # other curses inits goes here...

    def _set_color_pairs(self):
        pair_no = 0
        colors = {}

        for i in range(curses.COLORS):
            for j in range(curses.COLORS):
                pair_no += 1
                curses.init_pair(pair_no, i, j)
                color_no = curses.color_pair(pair_no)

                color = (i, j)  # color = (fg, bg)
                colors.update([(color, color_no)])

        return colors

    def run(self):
        """Run the terminal GUI application.
        """

        curses.wrapper(self.__app__)
        if not self._unblock:
            curses.cbreak()

            self._stdscr.getch()

            curses.nocbreak()
            curses.endwin()
