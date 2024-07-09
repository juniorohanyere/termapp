import curses
from curses import panel

from ._layout import Layout


class LinearLayout(Layout):
    def __init__(self, layout=None, **kwargs):
        """None means to fit content (curses.window.resize is called)
        0 means to fill parent
        """

        kw = {'size': 0, 'anchor': None, 'orient': 'horizontal', 'wrap': False,
              'color': None, 'padding': 0}

        for key, value in kwargs.items():
            if key not in kw.keys():
                error = 'LinearLayout.__init__() '
                error += f"got an unexpected keyword argument '{key}'"

                raise TypeError(error)

            kw[key] = value

        super().__init__(layout, kw)

        self._layout = layout if layout is None else self
        self._height = kw.get('height'), self._width = kw.get('width')
        self._anchor_y = kw.get('anchor_y'), self._anchor_x = kw.get('anchor_x'
                                                                    )
        self._fg = kw.get('fg'), self._bg = kw.get('bg')
        self._y, self._x = 0, 0     # current anchor position for children
        self._orient = kw.get('orient')
        self._padding_l, self._padding_r, self._padding_t, self._padding_b  = \
            (kw.get('padding_l'), kw.get('padding_r'), kw.get('padding_t'), kw.
             get('padding_b'))

        # now create a new view as the layout
        self._win, self._pan = self._create_layout(master, height, width,
                                                   anchor_y, anchor_x, fg, bg)

    def set_size(self, height, width):
        """Set or reset the layout size.
        """

        self._win.resize(height, width)
        self._win.refresh()

    def add_widget(self, widget):
        if isinstance(widget, Label):
            text = widget._text
            height, width = widget._height, widget._width
            anchor_y, anchor_x = self._y, self._x
            fg, bg = widget.fg, widget.bg
            pd_l, pd_r, pd_t, pd_b = (widget._padding_l, widget.padding_r,
                                      widget.padding_t, widget.padding_b)

            self._create_label(text, height, width, anchor_y, anchor_x, fg, bg)

            self._x += width + pd_l + pd_r if self._orient == 'horizontal' \
                else 0
            self._y += height + pd_t + pd_b if self._orient == 'vertical' \
                else 0
