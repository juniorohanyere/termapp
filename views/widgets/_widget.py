import curses
from curses import panel


class Widget:
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._color_pair_no = 0

    def _create_widget(self, master, fg, bg, *args):
        """Creates a new widget object.

        Args:
            master (obj): layout object.
            fg (int): foreground color of the widget.
            bg (int): background color of the widget.
            height (int): height of the widget.
            width (int): width of the widget.
            anchor_y (int): vertical position to anchor the widget.
            anchor_x (int): horizontal position to anchor the widget.

        Return:
            return a tuple object containing a curses window and a curses
            panel.
        """

        win = master.derwin(args)
        self.set_color(fg, bg)

        pan = panel.new_panel(win)
        pan.hide()

        return (win, pan)

    def _create_label(self):
        """TODO: text alignment to center, left, right, top, bottom, ...
                 text fonts (style, weight, size)
        """

        master = self._master
        height, width = self._kwargs.get('size')
        y, x = self._kwargs.get('anchor')
        fg, bg = self._kwargs.get('color')
        text = self._kwargs.get('text')

        self._win, self._pan = self._create_widget(master, fg, bg, height,
                                                   width, y, x)
        if text:
            self._win.addstr(text)

        self._win.refresh()

    def _set_color_pair(self, fg, bg):
        """Initialize color pair to be used by a widget.

        Args:
            fg (int): foreground color (0 to (curses.COLORS - 1))
            bg (int): background color (0 to (curses.COLORS - 1))

        Return:
            return the pair number.
        """

        self.color_pair_no += 1
        curses.init_pair(self.color_pair_no, fg, bg)

        return curses.color_pair(self.color_pair_no)

    def set_color(self, fg, bg):
        """Sets or resets the foreground color and background color of the
        widget.
        """

        pair_no = self._set_color_pair(fg, bg)
        self._win.bkgd(' ', pair_no)

        self._kwargs['color'] = (fg, bg)
