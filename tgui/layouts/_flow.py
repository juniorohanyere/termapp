"""Module to handle layouts.
"""

import curses
from curses import panel

from ..widgets import Label


class FlowLayout:
    def __init__(self, **kwargs):
        """Initialize self. See help(type(self)) for accurate signature.
        """

        kw = {'master': None, 'height': 0, 'width': 0, 'pos_y': 0, 'pos_x': 0}

        for key in kwargs:
            if key not in kw.keys():
                err = f'FlowLayout object has no attribute {key}'
                raise AttributeError(f'{err}')

                return 1

            kw[key] = kwargs.get(key)

        self.master = kw.get('master')
        if self.master is None:
            win = curses.newwin(0, 0, 0, 0)
        else:
            win = self.master.derwin(0, 0, 0, 0)

        pan = panel.new_panel(win)

        self.scr = (win, pan)

    def __add_label__(self, win, pan):
        """
        """

    def set_background(self, color):
        """Sets the background color of the layout.
        """

    def hide(self):
        """Make layout invisible, together with all its children widget.
        """

        _, pan = self.scr

        pan.hide()

    def show(self):
        """Make layout visible, together with all its children widget.
        """

        _, pan = self.scr

        pan.show()
