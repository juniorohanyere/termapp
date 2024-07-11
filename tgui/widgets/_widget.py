"""Base widget module.
"""

import asyncio
import curses
from curses import panel
import os

from .. import _tgui

class Widget:
    """Base widget class.
    """

    def __init__(self, layout, **kwargs):
        """Initialize self. See help(type(self)) for accurate signature.

        Args:
            kwargs (dict): dict containing keyworded arguments.
        """

        self._layout = layout
        self._kwargs = kwargs

        self._win, self._pan = None, None

    def _create_widget(self, color, *args):
        """Creates a new widget object.

        Args:
            layout (obj): layout object on which the widget is to be created.
            fg (int): foreground color of the widget.
            bg (int): background color of the widget.
            height (int): height of the widget.
            width (int): width of the widget.
            y: vertical position to anchor the widget.
            x: horizontal position to anchor the widget.
        """

        self._win = self._layout._win.derwin(*args)
        self.set_color(color)

        self._pan = panel.new_panel(self._win)
        self.hide()

    def _create_label(self):
        """create a new label.
        """

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
            error = 'anchor widget at next available position'
            raise NotImplementedError(error)

        elif isinstance(anchor, tuple):
            y, x = anchor
        else:
            y, x = anchor, anchor

        self._create_widget(color, height, width, y, x)
        # based on multiline and alignment
        self._win.addstr(0, 0, text)

    def set_color(self, color):
        """Set or reset the foreground and background color of the widget.
        """

        if color is None:
            # TODO use the terminal default display color
            fg, bg = curses.COLOR_BLACK, curses.COLOR_WHITE
        elif isinstance(color, tuple):
            fg, bg = color
        else:
            fg, bg = color, color

        color_pair = (fg, bg)
        pair_no = self._layout._color_pairs.get(color_pair)
        self._win.bkgd(' ', pair_no)

        self._kwargs['color'] = color_pair

    def show(self):
        self._pan.show()
        self._win.refresh()

    def hide(self):
        self._pan.hide()
        self._win.refresh()
