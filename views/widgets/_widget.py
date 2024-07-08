"""Module to handle widget.
"""

import asyncio
import curses
from curses import panel
import os


class Widget:
    """Base widget class.
    """

    def __init__(self, **kwargs):
        """Initialize self. See help(type(self)) for accurate signature.

        Args:
            kwargs: variable length keyworded arguments.
        """

        self._kwargs = kwargs
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

        Return:
            return a tuple object containing a curses window and a curses
            panel.
        """

        win = master._win.derwin(args)
        self.set_color(fg, bg)

        pan = panel.new_panel(win)
        pan.hide()

        return (win, pan)

    def _create_label(self):
        """create a new label.
        """

        master = self._master
        height, width = self._kwargs.get('size')
        y, x = self._kwargs.get('anchor')
        fg, bg = self._kwargs.get('color')
        text = self._kwargs.get('text')

        self._win, self._pan = self._create_widget(master, fg, bg, height,
                                                   width, y, x)
        if text:
            # based on multiline and alignment
            self._win.addstr(text)

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
