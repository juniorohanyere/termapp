"""Module to handle widget.
"""

import asyncio
import curses
from curses import panel
import os


class Widget:
    """Base widget class.
    """

    def __init__(self, a_dict={}):
        """Initialize self. See help(type(self)) for accurate signature.

        Args:
            kwargs: variable length keyworded arguments.
        """

        self._kwargs = a_dict
        self._color_pair_no = 0

    def _create_widget(self, master, fg, bg, *args):
        """Creates a new widget object.

        Args:
            master (obj): layout object on which the widget is to be created.
            fg (int): foreground color of the widget.
            bg (int): background color of the widget.
            height (int): height of the widget.
            width (int): width of the widget.
            y: vertical position to anchor the widget.
            x: horizontal position to anchor the widget.
        """

        self._win = master._win.derwin(*args)
        self.set_color(fg, bg)

        self._pan = panel.new_panel(self._win)
        self.hide()

    def _create_label(self):
        """create a new label.
        """

        master = self._master
        size = self._kwargs.get('size')
        anchor = self._kwargs.get('anchor')
        color = self._kwargs.get('color')
        text = self._kwargs.get('text')

        text = text if text else ''

        if size is None:
            # wrap content
            height, width = 1, len(text) + 1
        elif isinstance(size, tuple):
            height, width = size
        else:
            height, width = size, size

        if anchor is None:
            y, x = 0, 0     # XXX
        elif isinstance(anchor, tuple):
            y, x = anchor
        else:
            y, x = anchor, anchor

        if color is None:
            fg, bg = curses.COLOR_BLACK, curses.COLOR_WHITE
        elif isinstance(color, tuple):
            fg, bg = color
        else:
            fg, bg = color, color

        self._create_widget(master, fg, bg, height, width, y, x)
        # based on multiline and alignment
        self._win.addstr(0, 0, text)

    def _set_color_pair(self, fg, bg):
        """Initialize color pair for the widget.

        Args:
            fg (int): foreground color of the widget.
            bg (int): background color of the widget.

        Return:
            return the pair number of the color.
        """

        self._color_pair_no += 1
        curses.init_pair(self._color_pair_no, fg, bg)

        return curses.color_pair(self._color_pair_no)

    def set_color(self, fg, bg):
        """Set or reset the foreground and background color of the widget.
        """

        pair_no = self._set_color_pair(fg, bg)
        self._win.bkgd(' ', pair_no)

        self._kwargs['color'] = (fg, bg)

    def show(self):
        self._pan.show()
        self._win.refresh()

    def hide(self):
        self._pan.hide()
        self._win.refresh()
