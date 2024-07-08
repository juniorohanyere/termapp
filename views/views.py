"""Module to handle views.
"""

import asyncio
import curses
import curses.panel

#from .. import controllers
from controllers import protocol


class Widgets:
    """Widget class.
    """

    def __init__(self, *args, **kwargs):
        """Initialize self. See help(type(self)) for accurate signature.
        """
        self.color_pair_no = 0

    def create_panel(self, height, width, y, x):
        """Create a new panel with a specific height and width, while providing
           the offest to anchor the panel window.

        Args:
            height (int): height of the panel window.
            width (int): width of the panel window.
            y (int): vertical position to anchor the panel window.
            x (int): horizontal position to anchor the panel window.

        Return:
            return a tuple containing a window object and a panel object.
        """

        win = curses.newwin(height, width, y, x)
        win.erase()

        pan = curses.panel.new_panel(win)

        return win, pan

    def about(self, parent=None, fg=curses.COLOR_WHITE, bg=57):
        """Widget for the info about a host/server.

        Args:
            parent (window): (optional) placeholder for the widget to create.
            fg (int): (optional) foreground color for the widget. Values from 0
            to (curses.COLORS - 1).
            bg (int): (optional) background color for the widget. Values from 0
            to (curses.COLORS - 1).

        Return:
            return nothing.
        """

        parent = parent if parent else self.stdscr

        y, x = parent.getmaxyx()
        win, panel = self.create_panel(int(y / 2), x, 0, 0)

        pair_no = self.set_color(fg, bg)
        win.bkgd(' ', pair_no)

        win.attron(curses.A_BOLD)
        y, x = win.getmaxyx()

        r0 = '▀█▀ █▀▀ █░█ █▀█ ▀█▀'
        r1 = '░█░ █▄▄ █▀█ █▀█ ░█░'

        text = r0 + '\n' + r1

        y = int(y / 2)
        win.addstr(y, int(x / 2) - 10, r0)
        win.addstr(y + 1, int(x / 2) - 10, r1)

        win.addstr(y - 4, x - 3, u'\u25CF')
        win.addstr(y - 3, x - 3, '\u25CF')
        win.addstr(y - 2, x - 3, '\u25CF')

        win.attroff(curses.A_BOLD)

        curses.panel.update_panels()

        return win, panel

    def refresh(self, win=None):
        """Refresh a window object.

        Args:
            win (window): (optional) the window object to refresh. Defaults to
            stdscr.
        """

        win = win if win else self.stdscr

        win.refresh()

    def set_color(self, fg, bg):
        """Initialize color pair to be used by a widget.

        Args:
            fg (int): foreground color (0 to (curses.COLORS - 1))
            bg (int): background color (0 - curses.COLORS - 1))

        Return:
            return the pair number.
        """

        self.color_pair_no += 1
        curses.init_pair(self.color_pair_no, fg, bg)
        pair_no = curses.color_pair(self.color_pair_no)

        return pair_no

    def status_bar(self, parent=None, fg=curses.COLOR_WHITE, bg=60):
        """Status bar: displays the status of the connection, whether it's
           currently connecting, connected, or connection lost, etc.

        Args:
            parent (window): (optional) placeholder for the widget to create.
            fg (int): (optional) foreground color for the widget. Values from 0
            to (curses.COLORS - 1).
            bg (int): (optional) background color for the widget. Values from 0
            to (curses.COLORS - 1).

        Return:
            return nothing.
        """

        parent = parent if parent else self.stdscr

        y, x = parent.getmaxyx()
        win, panel = self.create_panel(1, x, int(y / 2), 0)

        pair_no = self.set_color(fg, bg)
        win.bkgd(' ', pair_no)

        win.attron(curses.A_BOLD)
        y, x = win.getmaxyx()
        win.addstr(int(y / 2), 1,
                   'TODO: Searching for hosts... (3 hosts found)')
        win.addstr(int(y / 2), x - 4, '57%')
        # win.attroff(curses.A_BOLD)

        curses.panel.update_panels()

        return win, panel


class Home(Widgets):
    def __init__(self, *args, **kwargs):
        """Initializs self. See help(type(self)) for accurate signature.
        """

        super().__init__(args, kwargs)

        self.protocol = protocol.Protocol()

        self.windows = []
        self.panels = []

    def main(self, stdscr):
        """
        """

        asyncio.run(self.home(stdscr))

    async def home(self, stdscr):
        self.stdscr = stdscr

        curses.curs_set(0)

        pair_no = self.set_color(57, curses.COLOR_WHITE)
        self.stdscr.bkgd(' ', pair_no)

        y, x = self.stdscr.getmaxyx()
        #self.stdscr.addstr(y - 3, 2, '██████')
        self.stdscr.addstr(y - 2, 2, '██████')
        self.stdscr.addstr(y - 1, 2, '▀▀▀▀▀▀')

        win, pan = self.about(self.stdscr)
        win1, pan1 = self.status_bar(self.stdscr)

        """
        flag, self.hostnames, self.hosts = await self.protocol.get_active_hosts()
        if flag is False:
            # change status bar string.
            win1.clear()
            y, x = win1.getmaxyx()
            win1.addstr(int(y / 2), 1, 'You\'re not connected to a local network')
        """

        self.windows += [win, win1]
        self.panels += [pan, pan1]

        win.refresh()

        win1.refresh()

        win.getch()
        # XXX test

        self.stdscr.getch()

        self.refresh()

    def show(self):
        """Display the home view/screen.
        """

    def hide(self):
        """Hide the home screen.
        """

        for panel in self.panels:
            panel.hide()

curses.wrapper(Home().main)
