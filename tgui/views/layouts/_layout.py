import curses
from curses import panel

from .tgui import TGUI

class Layout(TGUI):
    def __init__(self, **kwargs):
        """Initialize self. See help(type(self)) for accurate signature.
        """

        kw = {'master': None, 'height': 0, 'width': 0, 'y': 0, 'x': 0,
              'fg': None, 'bg': None, 'orient': None, 'pad_l': 1, 'pad_r': 1,
              'pad_t': 1, 'pad_b': 1}

        for key, value in kwargs.items():
            if key not in kw.keys():
                error = f'{cls}.__init__() got an unexpected keyword argument '
                error += f"'{key}'"

                raise TypeError(strerr)

            kw[key] = value

        super(Layout, self).__init__(a_dict=kw)

        self._master = kw.get('master')
        self._height, self._width = kw.get('height'), kw.get('width')
        self._y, self._x = kw.get('y'), kw.get('x')
        self._fg, self._bg = kw.get('fg'), kw.get('bg')
        # current anchor position for children
        self._cur_y, self._cur_x = 0, 0
        self._orient = kw.get('orient')
        self._pad_l, self._pad_r, self._pad_t, self._pad_b  = (kw.get('pad_l'),
                                                               kw.get('pad_r'),
                                                               kw.get('pad_t'),
                                                               kw.get('pad_b'))

    def _create_label(self, master, text, height, width, anchor_y, anchor_x,
                      fg, bg)
        """TODO: text alignment to center, left, right, top, bottom, ...
                 text fonts (style, weight, size)
        """

        win, pan = self._create_view(master, height, width, anchor_y, anchor_x,
                                     fg, bg)
        win.addstr(text)

    def _create_view(self, master, height, width, anchor_y, anchor_x, fg, bg):
        if master is None:
            win = curses.newwin(height, width, anchor_y, anchor_x)
            win.bkgd(' ', 1)    # TODO
        else:
            win = master.derwin(height, width, anchor_y, anchor_x)

        pan = panel.new_panel(win)

        return (win, pan)
