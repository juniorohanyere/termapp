import curses
from curses import panel

from .. import _tgui
from .._tgui import TGUI


class Layout(TGUI):
    """Base layout class.
    """

    def __init__(self, **kwargs):
        """Initialize self. See help(type(self)) for accurate signature.
        """

        super().__init__()

        self._kwargs = kwargs

    def _create_layout(self, layout, fg, bg, *args):
        """Create a new layout.
        """

        if layout is None:
            self._win = self._stdscr.derwin(*args)
        else:
            self._win = layout._win.derwin(*args)

        self._pan = panel.new_panel(self._win)

        self.set_color(fg, bg)

        self.hide()

    def _create_linear(self):
        """Create a new linear layout.
        """

        size = self._kwargs.get('size')
        orient = self._kwargs.get('orient')
        wrap = self._kwargs.get('wrap')
        color = self._kwargs.get('color')
        # TODO padding = self._kwargs.get('padding')

        # current anchor position for widgets or sub-layouts
        self._cur_y, self._cur_x = 0, 0

        if size is None:
            error = 'wrap content: get the size of all widgets and sub-layouts'

            raise NotImplementedError(error)

        if isinstance(size, tuple):
            height, width = size
        else:
            height, width = size, size

        if anchor is None:
            error = 'anchor layout at next available position'

            raise NotImplementedError(error)

        if isinstance(anchor, tuple):
            y, x = anchor
        else:
            y, x = anchor, anchor

        if color is None:
            # TODO use the terminal default display color
            fg, bg = curses.COLOR_BLACK, curses.COLOR_WHITE
        elif isinstance(color, tuple):
            fg, bg = color
        else:
            fg, bg = color, color

        self._create_layout(self.layout, fg, bg, height, width, y, x)

    def _set_color_pair(self, fg, bg):
        """Initialize color pair for the layout.

        Args:
            fg (int): foreground color for the layout.
            bg (int): background color for the layout.

        Return:
            return the pair number of the color.
        """

        _COLOR_PAIR_NO += 1
        curses.init_pair(self._color_pair_no, fg, bg)
